# LabelBoxDatasets

## Installation for internal use only

```bash
pip install git+https://github.com/RevoVet/LabelBoxDatasets.git
```

## Usage

### Load Module
```python
from LabelBoxDatasets import LabelBoxDataset
```

### Instantiate Class
```python
lbls = LabelBoxDataset(YOUR_API_KEY)
```

### Move Data to Labelbox Project Folder
```python
lbls.move_blobs('some-origin-bucket', 'revovet-client-labelbox')
```

### Create a list containing all the file names and gs:// paths

```python
lbls.get_filenames_frombucket('revovet-client-labelbox')
```

### Generate the Labelbox dataset

```python
lbls.generate_dataset('SomeDataSetName')
``````


## Docstring

```python
help(LabelBoxDataset)
```
