cmake_minimum_required(VERSION 3.10.0)
project(ticker_loader VERSION 0.1.0 LANGUAGES C)

include_directories("C:/msys64/ucrt64/include")
link_directories("C:/msys64/ucrt64/lib")

add_executable(ticker_loader ticker_loader.c)

target_link_libraries(ticker_loader PRIVATE curl cjson)