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
    bmdiff.read_bm(bm, band="k")
    for bm in ("data/union0.dat",
                "data/union1.dat",
                "data/union2.dat")]

union = bmdiff.union(bms, band="k")

```
