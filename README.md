# Lineage Connectomics

Watch our NeuroMatch 4.0 Talk!

[![YouTube Link to Talk](https://user-images.githubusercontent.com/693511/144762457-0e3b543b-957b-4d99-890d-421a69ccff77.png)](http://www.youtube.com/watch?v=fEv94br2V00 "NeuroMatch 4.0: Predicting the connectome with neuron family trees — Jordan Matelsky")

## Data

### Connectomes

#### `witvliet2021-Dataset8.graphml`

This dataset is downloaded at runtime from MossDB. A copy is cached in `data/`.

### Lineages

#### `bhatla-lineage.json`

This dataset was generated by evaluating the JavaScript object provided [here](http://wormweb.org/js/json-celllineage.js) and copying to JSON. This can be most easily done by pasting the data into a browser JS console:

```js
copy(JSON.stringify(...));
```

Or by calling the `getJson()` function on [this page](http://wormweb.org/celllineage):

```js
copy(JSON.stringify(getJson()));
```

### Cell Locations

We need a way to determine a cell location for each cell so that we can talk meaningfully about cell "distances" in Euclidean space. Unfortunately, the easiest way I can think of to do this is to go to the OpenWorm .blend Blender 3D model and capture the origins of all neuron cell meshes.

The script to accomplish this is stored in `preprocessing/get-blender-centroids.py`. Note that this Python code will NOT run in "plain" Python; it MUST be run from inside Blender.

You can download the source material from [this website](http://canopus.caltech.edu/virtualworm/Virtual%20Worm%20Blend%20File/).

We use the latest Feb 2012 version.

### Usage

To create the figures in `figs/`, the `Analysis.ipynb` notebook is run twice; first with the `NULL_MODEL` parameter set to `True`, and then with the `NULL_MODEL` parameter set to `False`. This creates `fig-grouped-distance-null.svg` and `fig-grouped-distance.svg` in `figs/`
