cmake_minimum_required(VERSION 3.18)
project(pikocore_native_tests CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

function(AddPikocoreNativeTest TestName SourceFiles IncludeDirs)
  add_executable(${TestName}
    "${TestName}.cpp"
    ${SourceFiles}
  )
  target_include_directories(${TestName} PRIVATE ${IncludeDirs})
  target_compile_options(${TestName} PRIVATE -Wall -Wextra -Werror)
  add_test(NAME ${TestName} COMMAND ${TestName})
endfunction()

enable_testing()
AddPikocoreNativeTest(
  clock_sync_test
  ../src/ClockSync.cpp
  ../src
)
AddPikocoreNativeTest(
  tempo_knob_test
  tempo_knob_test.cpp
  ../doth
)
