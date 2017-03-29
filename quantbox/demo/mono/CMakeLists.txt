cmake_minimum_required(VERSION 2.6)

project(perfbot4)

set(EXECUTABLE_OUTPUT_PATH  bin)

find_package(LibXml2 REQUIRED)
include_directories(${LIBXML2_INCLUDE_DIR})
include_directories(/home/danilk/demo2/sdk/include)
link_directories(/home/danilk/demo2/sdk/lib)
link_directories(/home/danilk/demo2/deps/lib)

set(SRC main.c process.c)

add_executable(${PROJECT_NAME} ${SRC})

target_link_libraries(${PROJECT_NAME} common node rt pthread order ui m instrdb cgate_core cgate_engine
   mdata_book_map cgate mdata)
