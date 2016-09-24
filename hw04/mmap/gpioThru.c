// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Read one gpio pin and write it out to another using mmap.
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
// Modified by Alvin koontz  24-Sept-2016
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
volatile int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
//    printf("%d\n",keepgoing);
	keepgoing = 0;
    printf( "\nCtrl-C pressed, trying to clean up and exit...\n" );
//    printf("%d\n",keepgoing);
}

int main(int argc, char *argv[]) {
    volatile void *gpio0_addr;
    volatile unsigned int *gpio0_oe_addr;
    volatile unsigned int *gpio0_datain;
    volatile unsigned int *gpio0_setdataout_addr;
    volatile unsigned int *gpio0_cleardataout_addr;
    volatile void *gpio1_addr;
    volatile unsigned int *gpio1_oe_addr;
    volatile unsigned int *gpio1_datain;
    volatile unsigned int *gpio1_setdataout_addr;
    volatile unsigned int *gpio1_cleardataout_addr;
    unsigned int reg;

    // Set the signal callback for Ctrl-C
    signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    printf("Mapping gpio 0 %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, GPIO0_SIZE);
    printf("Mapping gpio 1 %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, GPIO1_SIZE);

    gpio0_addr = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO0_START_ADDR);
    gpio1_addr = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);

    gpio0_oe_addr           = gpio0_addr + GPIO_OE;
    gpio0_datain            = gpio0_addr + GPIO_DATAIN;
    gpio0_setdataout_addr   = gpio0_addr + GPIO_SETDATAOUT;
    gpio0_cleardataout_addr = gpio0_addr + GPIO_CLEARDATAOUT;
    gpio1_oe_addr           = gpio1_addr + GPIO_OE;
    gpio1_datain            = gpio1_addr + GPIO_DATAIN;
    gpio1_setdataout_addr   = gpio1_addr + GPIO_SETDATAOUT;
    gpio1_cleardataout_addr = gpio1_addr + GPIO_CLEARDATAOUT;

    if( gpio1_addr == MAP_FAILED ||
        gpio0_addr == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }
    printf("GPIO0 mapped to %p\n", gpio0_addr);
    printf("GPIO0 OE mapped to %p\n", gpio0_oe_addr);
    printf("GPIO0 SETDATAOUTADDR mapped to %p\n", gpio0_setdataout_addr);
    printf("GPIO0 CLEARDATAOUT mapped to %p\n", gpio0_cleardataout_addr);
    printf("GPIO1 mapped to %p\n", gpio1_addr);
    printf("GPIO1 OE mapped to %p\n", gpio1_oe_addr);
    printf("GPIO1 SETDATAOUTADDR mapped to %p\n", gpio1_setdataout_addr);
    printf("GPIO1 CLEARDATAOUT mapped to %p\n", gpio1_cleardataout_addr);

    // Set USR3 to be an output pin
    reg = *gpio1_oe_addr;
    printf("GPIO1 configuration: %X\n", reg);
    reg &= ~USR3;       // Set USR3 bit to 0
    *gpio1_oe_addr = reg;
    printf("GPIO1 configuration: %X\n", reg);

/*    printf("Start copying GPIO_07 to GPIO_03\n");
    while(keepgoing) {
    	if(*gpio_datain & GPIO_07) {
            *gpio_setdataout_addr= GPIO_03;
    	} else {
            *gpio_cleardataout_addr = GPIO_03;
    	}
        //usleep(1);
    }
*/
    printf("Start blinking LED USR3\n");
    while(keepgoing) {
//        if(keepgoing ==0){
//            printf("ON\n");
//            break;
//        }
        if(!(*gpio0_datain & P9_11)){
            *gpio1_setdataout_addr = USR3;
        }else{
            *gpio1_cleardataout_addr = USR3;
        }
    }

    munmap((void *)gpio1_addr, GPIO1_SIZE);
    munmap((void *)gpio0_addr, GPIO0_SIZE);
    close(fd);
    return 0;

}
