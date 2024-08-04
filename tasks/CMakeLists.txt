cmake_minimum_required(VERSION 3.10)
project(Problems VERSION 1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# TASKS
set(TASKS_DIR "assert-tasks")
file(GLOB_RECURSE ASSERT_TASKS_CPP_SRCS RELATIVE "${PROJECT_SOURCE_DIR}/${TASKS_DIR}" "${PROJECT_SOURCE_DIR}/${TASKS_DIR}/*/*.cpp")

foreach(SRC_FILE ${ASSERT_TASKS_CPP_SRCS})
    get_filename_component(TARGET_FILENAME ${SRC_FILE} NAME_WE)
    get_filename_component(TARGET_DIR ${SRC_FILE} DIRECTORY)
    set(TARGET_NAME "${TARGET_DIR}_${TARGET_FILENAME}")

    add_executable("${TARGET_NAME}.e" "${TASKS_DIR}/${SRC_FILE}")
    set_target_properties("${TARGET_NAME}.e" PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${TASKS_DIR}/${TARGET_DIR}/bin"
    )
    target_compile_options("${TARGET_NAME}.e" PRIVATE -Wall -Wextra -pedantic -Wconversion)
endforeach()
