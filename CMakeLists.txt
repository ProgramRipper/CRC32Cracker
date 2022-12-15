cmake_minimum_required(VERSION 3.0.0)
project(CRC32Craker VERSION 0.1.0)

if(CMAKE_SYSTEM_NAME MATCHES "Linux")
    link_libraries(m)
endif(CMAKE_SYSTEM_NAME MATCHES "Linux")


add_executable(crack main.c)
