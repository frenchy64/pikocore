#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "tempo_knob.h"

namespace {
constexpr uint16_t minKnobValue = 0;
constexpr uint16_t maxKnobValue = 4095;
constexpr uint16_t minKnobIncrement = 77;
constexpr uint16_t largestKnobForMinTempo = minKnobIncrement+1;
constexpr uint16_t tempoIncrement = 5;
constexpr uint16_t numTempos = 52;
constexpr uint16_t minTempo = 50;
constexpr uint16_t maxTempo = 305;

void testAllTemposAreReachableFromFirstTempo() {
  printf("top of testAllTemposAreReachableFromFirstTempo\n");
  fflush(stdout);
  assert(bpm_set_new_from_knob(largestKnobForMinTempo) == minTempo);
  assert(bpm_set_new_from_knob(largestKnobForMinTempo+1) == minTempo+tempoIncrement);
  for (uint16_t initial_knob_value = 0; initial_knob_value <= largestKnobForMinTempo; ++initial_knob_value) {
    printf("initial_knob_value: %d\n", initial_knob_value);
    fflush(stdout);
    uint16_t knob_value = initial_knob_value;
    uint16_t expected_tempo = minTempo;
    uint16_t found_tempos = 0;

    assert(bpm_set_new_from_knob(knob_value) == expected_tempo);

    // if we increment the knob by the smallest amount, we should be able to reach
    // each tempo
    for (int i = 0; i < numTempos; ++i) {
      for (int attempts = 0; attempts < 3; ++attempts) {
        printf("attempt: %d\n", attempts);
        uint16_t actual_tempo = bpm_set_new_from_knob(knob_value);
        if (actual_tempo >= expected_tempo) {
          printf("match! knob_value: %d, expected_tempo: %d, actual_tempo: %d\n", knob_value, expected_tempo, actual_tempo);
          break;
        }
        printf("miss! knob_value: %d, expected_tempo: %d, actual_tempo: %d, initial_knob_value: %d\n", knob_value, expected_tempo, actual_tempo,
            initial_knob_value);
        if (knob_value + minKnobIncrement <= maxKnobValue) knob_value += minKnobIncrement;
      }
      uint16_t actual_tempo = bpm_set_new_from_knob(knob_value);
      printf("expected_tempo: %d, actual_tempo: %d, knob_value: %d\n", expected_tempo, actual_tempo, knob_value);
      fflush(stdout);
      assert(actual_tempo == expected_tempo);
      found_tempos++;
      expected_tempo += tempoIncrement;
      if (knob_value + minKnobIncrement <= maxKnobValue) knob_value += minKnobIncrement;
      if (expected_tempo > maxTempo) expected_tempo = maxTempo;
    }
    uint16_t actual_tempo = bpm_set_new_from_knob(knob_value);
    printf("final actual_tempo: %d\n", actual_tempo);
    fflush(stdout);
    assert(actual_tempo == maxTempo);
    printf("found_tempos: %d, initial_knob_value: %d\n", found_tempos, initial_knob_value);
    fflush(stdout);
    assert(found_tempos == numTempos);
  }
}
}  // namespace

int main(void) {
  testAllTemposAreReachableFromFirstTempo();
  printf("knob_test: all assertions passed\n");
  fflush(stdout);
  return 0;
}
