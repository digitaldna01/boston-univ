/* cand: About as simple as it gets. A C function `cand` that returns
   a signed 8 byte integer that is the bitwise AND of two 8 byte
   signed integers x and y */
long long
cand(long long x, long long y) {
  // & is the bitwise and the inputs see C bitwise operators for
  // more info
  return x & y;
}
