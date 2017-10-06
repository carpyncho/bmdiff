# Band-Merge Diff
Differences between band merges

## Ussage

```bash
python bmdiff.py input.dat --filters flt0.dat flt1.dat -o out.txt

```

### From script

```python
import bmdiff

input = bmdiff.read_bm("input.dat")
flt = [
    bmdiff.read_bm("flt0.dat"),
    bmdiff.read_bm("flt1.dat")]

diff = bmdiff.difference(input, flt)

```
