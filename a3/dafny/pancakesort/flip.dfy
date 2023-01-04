// flips (i.e., reverses) array elements in the range [0..num]
method flip (a: array<int>, num: int)
requires a.Length > 0;
requires 0 <= num < a.Length;
// Arrays contain same number of elements
ensures multiset(old(a[..])) == multiset(a[..]);
// swap from i to num
ensures forall k :: 0<=k<=num ==> a[k] == old(a[num-k]);
// num to a.Length remain the same
ensures forall u :: num<u<a.Length ==> a[u] == old(a[u]);
modifies a;
{
  var tmp:int;
  var i := 0;
  var j := num;
  while (i < j)
  decreases j-i;
  invariant i+j == num;
  invariant multiset(old(a[..])) == multiset(a[..]);
  // think about what will happen during each loop
  // whatever outside num is not changed
  invariant forall u :: a.Length>u>num ==>a[u] == old(a[u]);
  // whatever before i has been flipped
  invariant forall u :: 0<=u<i ==> a[u] == old(a[num-u]);
  // whatever i<=u<=j has not yet changed
  invariant forall u :: i<=u<=j ==> a[u] == old(a[u]);
  // whatever j<u<=num has been changed
  invariant forall u:: j<u<=num ==> a[u] == old(a[num-u]);
  {
    tmp := a[i];
    a[i] := a[j];
    a[j] := tmp;
    i := i + 1;
    j := j - 1;
  }
}
