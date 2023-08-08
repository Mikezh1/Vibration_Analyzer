################################################################################
# 自动生成的文件。不要编辑！
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

-include ../makefile.init

RM := rm -rf

# 此处定义了参与生成的所有源
-include sources.mk
-include Middlewares/Third_Party/FreeRTOS/Source/portable/MemMang/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/subdir.mk
-include Drivers/STM32F1xx_HAL_Driver/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := RTOS_MPU6050_FFT_2Tasks
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# 将这些工具调用的输入和输出添加到构建变量 
EXECUTABLES += \
RTOS_MPU6050_FFT_2Tasks.elf \

MAP_FILES += \
RTOS_MPU6050_FFT_2Tasks.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
RTOS_MPU6050_FFT_2Tasks.list \


# 所有目标
all: main-build

# 主构建目标
main-build: RTOS_MPU6050_FFT_2Tasks.elf secondary-outputs

# 工具调用
RTOS_MPU6050_FFT_2Tasks.elf RTOS_MPU6050_FFT_2Tasks.map: $(OBJS) $(USER_OBJS) D:\Root_Folder\temp_program\019_STM32_project\STM32CubeIDE\workspace_1.12.1\RTOS_MPU6050_FFT_2Tasks\STM32F103C8TX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-gcc -o "RTOS_MPU6050_FFT_2Tasks.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m3 -T"D:\Root_Folder\temp_program\019_STM32_project\STM32CubeIDE\workspace_1.12.1\RTOS_MPU6050_FFT_2Tasks\STM32F103C8TX_FLASH.ld" --specs=nosys.specs -Wl,-Map="RTOS_MPU6050_FFT_2Tasks.map" -Wl,--gc-sections -static --specs=nano.specs -mfloat-abi=soft -mthumb -u _printf_float -Wl,--start-group -lc -lm -Wl,--end-group
	@echo '已结束构建目标： $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo '已结束构建： $@'
	@echo ' '

RTOS_MPU6050_FFT_2Tasks.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "RTOS_MPU6050_FFT_2Tasks.list"
	@echo '已结束构建： $@'
	@echo ' '

# 其他目标
clean:
	-$(RM) RTOS_MPU6050_FFT_2Tasks.elf RTOS_MPU6050_FFT_2Tasks.list RTOS_MPU6050_FFT_2Tasks.map default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
