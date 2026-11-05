#include <cmath>

/**
 * knob_value is 0-4095.
 * there are 52 possible return values, the multiples of 5 from 50 to 305.
 * only called if knob_value has changed by at least 77 from the previous call.
 * you can always reach the immediately previous/next return value (if any) by decrementing/incrementing
 * knob_value by at least 77 (higher increments may be necessary).
 **/
inline uint16_t bpm_set_new_from_knob(uint16_t knob_value) {
  return floor((double)knob_value / (4096.0 / 52.0)) *
    5 +
    50;
}
