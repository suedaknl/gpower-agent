# oracle/

| file | what | ground truth? |
|---|---|---|
| `gpower_vectors.csv` | Inputs are pre-filled; **you fill output columns from the G\*Power GUI** (Windows) and save one screenshot per row in `oracle/screenshots/G##.png`. Leave outputs empty for rows where G\*Power rejects the input and write the message in `note`. | **yes** |
| `statsmodels_vectors.csv` | 1000+ scale vectors from `statsmodels` (fractional N). | no, scale only |
| `make_statsmodels_vectors.py` | regenerates the file above | |

Rows with empty outputs are skipped by the conformance report, so the report only counts real measurements.
Write the number of decimals G\*Power displays (e.g. `0.9501000`): the report compares to exactly that many decimals.
