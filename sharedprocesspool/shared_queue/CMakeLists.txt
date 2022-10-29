cmake_minimum_required(VERSION 3.0.0)
project(shared_queue VERSION 0.1.0)

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

include(CTest)
enable_testing()

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()


find_package(PythonInterp 3.6 REQUIRED)

# This goes after, since it uses PythonInterp as hint
find_package(PythonLibs 3.6 REQUIRED)



add_library(shared_queue ${CMAKE_SOURCE_DIR}/src/shared_queue.c)
include_directories(${CMAKE_SOURCE_DIR}/include)
set_target_properties(
    shared_queue
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "shared_queue"
        LINKER_LANGUAGE C
    )
target_link_libraries(shared_queue rt)

add_custom_command(TARGET shared_queue POST_BUILD
    COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/src/setup.py build
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Creating python shared memory queue extension"
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)

add_executable(runTests test/tests.cpp)
include_directories(${CMAKE_SOURCE_DIR}/include)
target_link_libraries(runTests ${GTEST_LIBRARIES} pthread shared_queue)
