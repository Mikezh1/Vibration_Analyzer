/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "fonts.h"
#include "ssd1306.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
typedef struct MPU6050
{
	int16_t Accel_X_RAW; //raw data of acceleration x (16384 means 1 g)
	int16_t Accel_Y_RAW; //raw data of acceleration y
	int16_t Accel_Z_RAW; //raw data of acceleration z

	//float Ax, Ay, Az;

	void (*Init)(void);
	void (*Read_Accel)(struct MPU6050_t*);
}MPU6050_t;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define MPU6050_ADDR 0xD0 //(0b1101000 <<1) + 0
#define SMPLRT_DIV_REG 0x19
#define ACCEL_CONFIG_REG 0x1C
#define ACCEL_XOUT_H_REG 0x3B
#define TEMP_OUT_H_REG 0x41
#define PWR_MGMT_1_REG 0x6B
#define WHO_AM_I_REG 0x75

#define NPT 256 //number of samples
#define Fs 500 //Sample frequency
#define PI2 6.28318530717959 //2Pi
#define Freq_Increment (Fs*1.0/NPT) //frequency resolution

#define BUFFER_SIZE NPT // buffer size of circular buffer
typedef struct {
	uint32_t buffer[BUFFER_SIZE];
    int head;  // point at the latest data
    int tail;  // point at the oldest data
    int count; // number of elements in the buffer
} CircularBuffer;
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN Variables */

//input array, output array and magnitude array(normalized absolute value)
uint32_t input[NPT], output[NPT], Mag[NPT/2];


CircularBuffer buffer; //the circular buffer
MPU6050_t imu1; // the Inertial Measurement Unit


extern I2C_HandleTypeDef hi2c1; //IIC1: OLED display
extern I2C_HandleTypeDef hi2c2; //IIC2: MPU6050
extern UART_HandleTypeDef huart1; //UART: communicate with the host computer

/* USER CODE END Variables */
osThreadId FFT_and_SendHandle;
osThreadId SampleHandle;
osMutexId myMutex01Handle;

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */
void MPU6050_Init (void)//(MPU6050_t *imu1)
{
	uint8_t check;
	uint8_t Data;
	char str[50];
	uint8_t stat;

	HAL_Delay(50);
	// check device ID WHO_AM_I

	stat=HAL_I2C_Mem_Read (&hi2c2, MPU6050_ADDR,WHO_AM_I_REG,1, &check, 1, 1000);
	if (stat != HAL_OK)
	{
		NVIC_SystemReset();
	}


	if (check == 0x68)  // 0x68 will be returned by the sensor if everything goes well
	{
		// power management register 0X6B we should write all 0's to wake the sensor up
		Data = 0;
		HAL_I2C_Mem_Write(&hi2c2, MPU6050_ADDR, PWR_MGMT_1_REG, 1,&Data, 1, 1000);

		// Set DATA RATE of 1KHz by writing SMPLRT_DIV register
		Data = 0x07;
		HAL_I2C_Mem_Write(&hi2c2, MPU6050_ADDR, SMPLRT_DIV_REG, 1, &Data, 1, 1000);

		// Set accelerometer configuration in ACCEL_CONFIG Register
		// XA_ST=0,YA_ST=0,ZA_ST=0, FS_SEL=0 -> �??????????????? 2g
		Data = 0x00;
		HAL_I2C_Mem_Write(&hi2c2, MPU6050_ADDR, ACCEL_CONFIG_REG, 1, &Data, 1, 1000);

		sprintf(str, "MPU6050 initialized.\r\n");
		HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);
	}
	else
	{
		sprintf(str, "The sensor is not MPU6050\r\n");
		HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);
		HAL_Delay(10);
	}

}


void MPU6050_Read_Accel (MPU6050_t *imu1)
{
	uint8_t Rec_Data[6];
	uint8_t stat;

	// Read 6 BYTES of data starting from ACCEL_XOUT_H register

	stat=HAL_I2C_Mem_Read (&hi2c2, MPU6050_ADDR, ACCEL_XOUT_H_REG, 1, Rec_Data, 6, 1000);

	if (stat != HAL_OK)
	{
		NVIC_SystemReset();
	}

	imu1->Accel_X_RAW = (int16_t)(Rec_Data[0] << 8 | Rec_Data [1]);
	imu1->Accel_Y_RAW = (int16_t)(Rec_Data[2] << 8 | Rec_Data [3]);
	imu1->Accel_Z_RAW = (int16_t)(Rec_Data[4] << 8 | Rec_Data [5]);

	/*** convert the RAW values into acceleration in 'g'
	     we have to divide according to the Full scale value set in FS_SEL
	     I have configured FS_SEL = 0. So I am dividing by 16384.0
	     for more details check ACCEL_CONFIG Register              ****/

//	imu1->Ax = imu1->Accel_X_RAW/16384.0;
//	imu1->Ay = imu1->Accel_Y_RAW/16384.0;
//	imu1->Az = imu1->Accel_Z_RAW/16384.0;
}

void PowerMag()
{
	int16_t lX,lY;
	uint16_t i;
	char str[50];
	float mag;
	// the magnitude
	for (i=0; i <NPT/2+1; i++)
	{
		lX= (output[i]<<16)>>16; //real part (LSB)
		lY= (output[i]>> 16);	//imaginary part
		mag = sqrtf(lX*lX+ lY*lY);//magnitude
		Mag[i]= mag*2;//for alternating component: mag*2

	}
	//for zero frequency component: mag=mag*2/2
	Mag[0] = Mag[0]>>1;// /2


}

void initCircularBuffer(CircularBuffer *cb)
{
    cb->head = 0;
    cb->tail = 0;
    cb->count = 0;
}

void addToCircularBuffer(CircularBuffer *cb, uint32_t data)
{
    cb->buffer[cb->head] = data;
    cb->head = (cb->head + 1) % BUFFER_SIZE; // increase head
    if (cb->count < BUFFER_SIZE) {
        cb->count++; // buffer not full, add count
    } else {
        cb->tail = (cb->tail + 1) % BUFFER_SIZE; // buffer is full, cover the oldest element
    }
}

int readFromCircularBuffer(CircularBuffer *cb)
{
    int data = cb->buffer[cb->tail];
    cb->tail = (cb->tail + 1) % BUFFER_SIZE; // increase tail
    if (cb->count > 0) {
        cb->count--; // decrease count
    }
    return data;
}

int getCircularBufferCount(CircularBuffer *cb)
{
    return cb->count;
}


void copyCircularBufferToArray(CircularBuffer *cb, int* array, int size)
{
    int originalCount = cb->count; // original number of elements
    int i;
    for (i = 0; i < size; i++) {
        array[i] = readFromCircularBuffer(cb);
    }
    cb->count = originalCount; // recover original number of elements
}

void printCircularBuffer(CircularBuffer *cb)
{
    int i;
    for (i = 0; i < BUFFER_SIZE; i++) {
        int index = (cb->tail + i) % BUFFER_SIZE; // the index of ele to be printed
        printf("Buffer[%d]: %d\n", i, cb->buffer[index]);
    }
}

int findMaxIndex(int arr[], int size)
{
    int maxIndex = 0; // store the index of the max. element

    for (int i = 1; i < size; i++) {
        if (arr[i] > arr[maxIndex]) {
            maxIndex = i; // update the index of the max. element
        }
    }

    return maxIndex;
}



/* USER CODE END FunctionPrototypes */

void FFT_and_Send_Task(void const * argument);
void Sample_Task(void const * argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/* GetIdleTaskMemory prototype (linked to static allocation support) */
void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize );

/* Hook prototypes */
void vApplicationStackOverflowHook(xTaskHandle xTask, signed char *pcTaskName);
void vApplicationMallocFailedHook(void);

/* USER CODE BEGIN 4 */
__weak void vApplicationStackOverflowHook(xTaskHandle xTask, signed char *pcTaskName)
{
   /* Run time stack overflow checking is performed if
   configCHECK_FOR_STACK_OVERFLOW is defined to 1 or 2. This hook function is
   called if a stack overflow is detected. */
	char str[50];
	sprintf(str, "Task stack overflow detected.%d\r\n");
	HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);
}
/* USER CODE END 4 */

/* USER CODE BEGIN 5 */
__weak void vApplicationMallocFailedHook(void)
{
   /* vApplicationMallocFailedHook() will only be called if
   configUSE_MALLOC_FAILED_HOOK is set to 1 in FreeRTOSConfig.h. It is a hook
   function that will get called if a call to pvPortMalloc() fails.
   pvPortMalloc() is called internally by the kernel whenever a task, queue,
   timer or semaphore is created. It is also called by various parts of the
   demo application. If heap_1.c or heap_2.c are used, then the size of the
   heap available to pvPortMalloc() is defined by configTOTAL_HEAP_SIZE in
   FreeRTOSConfig.h, and the xPortGetFreeHeapSize() API function can be used
   to query the size of free heap space that remains (although it does not
   provide information on how the remaining heap might be fragmented). */
	char str[50];
	sprintf(str, "MallocFailed\r\n");
	HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);
}
/* USER CODE END 5 */

/* USER CODE BEGIN GET_IDLE_TASK_MEMORY */
static StaticTask_t xIdleTaskTCBBuffer;
static StackType_t xIdleStack[configMINIMAL_STACK_SIZE];

void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer, StackType_t **ppxIdleTaskStackBuffer, uint32_t *pulIdleTaskStackSize )
{
  *ppxIdleTaskTCBBuffer = &xIdleTaskTCBBuffer;
  *ppxIdleTaskStackBuffer = &xIdleStack[0];
  *pulIdleTaskStackSize = configMINIMAL_STACK_SIZE;
  /* place for user code */
}
/* USER CODE END GET_IDLE_TASK_MEMORY */

/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */

  /* USER CODE END Init */
  /* Create the mutex(es) */
  /* definition and creation of myMutex01 */
  osMutexDef(myMutex01);
  myMutex01Handle = osMutexCreate(osMutex(myMutex01));

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* definition and creation of FFT_and_Send */
  osThreadDef(FFT_and_Send, FFT_and_Send_Task, osPriorityNormal, 0, 2000);
  FFT_and_SendHandle = osThreadCreate(osThread(FFT_and_Send), NULL);

  /* definition and creation of Sample */
  osThreadDef(Sample, Sample_Task, osPriorityNormal, 0, 128);
  SampleHandle = osThreadCreate(osThread(Sample), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

}

/* USER CODE BEGIN Header_FFT_and_Send_Task */
/**
  * @brief  Function implementing the FFT_and_Send thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_FFT_and_Send_Task */
void FFT_and_Send_Task(void const * argument)
{
  /* USER CODE BEGIN FFT_and_Send_Task */


	  char str[50];
	  int len;

	  int size;//size of Mag[]
	  int maxIndex;//the index of the max. element in Mag[]

	  int index=1;

	  SSD1306_Init();
	  SSD1306_GotoXY (0,0);
	  SSD1306_Puts ("Frequency:", &Font_11x18, 1);
	  SSD1306_UpdateScreen();

	  TickType_t pxPreviousWakeTime;
	  pxPreviousWakeTime = xTaskGetTickCount();

  /* Infinite loop */
  for(;;)
  {


	  if(buffer.count<NPT)//data not enough in the circular buffer
	  {

	  }
	  else//data enough
	  {

			uint32_t* input = (uint32_t*)calloc(NPT , sizeof(uint32_t));
  //		    if (input == NULL) {
  //		        printf("Memory allocation failed.\n");
  //		        return 1;
  //		    }


		  xSemaphoreTake(myMutex01Handle,portMAX_DELAY);//take the mutex
		  copyCircularBufferToArray(&buffer, input, BUFFER_SIZE);
		  xSemaphoreGive(myMutex01Handle);//release the mutex


		  cr4_fft_256_stm32(output, input, NPT);//FFT
		  free(input);

		  PowerMag();//calculate the magnitude of FFT result

		  size = sizeof(Mag) / sizeof(Mag[0]);

		  //the index of the max. element in Mag[]
		  //the frequency with the max. magnitude
		  maxIndex = findMaxIndex(Mag, size);

		  sprintf(str, "%.2f Hz     ", (float)(maxIndex*Freq_Increment));

		  SSD1306_GotoXY (0,30);
		  SSD1306_Puts (str, &Font_11x18, 1);
		  SSD1306_UpdateScreen();

		  //UART send
		  sprintf(str, "Start\r\n");
		  HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);

		  for(int i=0;i<NPT/2+1;i++)
		  {
			  sprintf(str, "%u\r\n", Mag[i]);
			  HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);
		  }


		  sprintf(str, "End\r\n");
		  HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);

//		  if(index==4)
//		  {
//			  sprintf(str, "------------------\r\n");
//			  HAL_UART_Transmit(&huart1,(uint8_t*)str,strlen(str),0XFFFF);
//		  }
//
//		  if(index<4)index++;
//		  else index=1;

	  }

	  vTaskDelayUntil(&pxPreviousWakeTime, 250);//time interval 250ms
  }
  /* USER CODE END FFT_and_Send_Task */
}

/* USER CODE BEGIN Header_Sample_Task */
/**
* @brief Function implementing the Sample thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_Sample_Task */
void Sample_Task(void const * argument)
{
  /* USER CODE BEGIN Sample_Task */
	uint32_t total_acc_16384;//16384 means 1 g

	initCircularBuffer(&buffer);

	MPU6050_t imu1=
		  {
				  .Accel_X_RAW=0,
				  .Accel_Y_RAW=0,
				  .Accel_Z_RAW=0,
				  .Init=MPU6050_Init,
				  .Read_Accel=MPU6050_Read_Accel
		  };

	  imu1.Init(); // must initialized after I2C2


	TickType_t pxPreviousWakeTime;
	pxPreviousWakeTime = xTaskGetTickCount();
  /* Infinite loop */
  for(;;)
  {
	  imu1.Read_Accel(&imu1);

	  total_acc_16384=sqrt(imu1.Accel_X_RAW*imu1.Accel_X_RAW+\
			  imu1.Accel_Y_RAW*imu1.Accel_Y_RAW+\
			  imu1.Accel_Z_RAW*imu1.Accel_Z_RAW);

	  xSemaphoreTake(myMutex01Handle,portMAX_DELAY);//take the mutex
	  addToCircularBuffer(&buffer, total_acc_16384);
	  xSemaphoreGive(myMutex01Handle);//release the mutex

	  vTaskDelayUntil(&pxPreviousWakeTime, 2);//time interval 2ms
  }
  /* USER CODE END Sample_Task */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */

