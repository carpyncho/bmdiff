# Band-Merge Diff and Union
Differences between band merges

### Difference

```python
import bmdiff

input = bmdiff.read_bm("input.dat")
flt = [
    bmdiff.read_bm("flt0.dat"),
    bmdiff.read_bm("flt1.dat")]

diff = bmdiff.difference(input, flt)

```

### Union

```python
import bmdiff

bms = filters = [
    bmdiff.read_bm("data/union0.dat", band="k"),
    bmdiff.read_bm("data/union1.dat", band="k"),
    bmdiff.read_bm("data/union2.dat", band="k")]

union = bmdiff.union(bms, band="k")

```
