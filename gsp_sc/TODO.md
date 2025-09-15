# TODO
- BUG in rendering the multi viewport, i have a single camera
- add sanity check on the np.ndarray shapes type hinting
  - https://github.com/ramonhagenaars/nptyping/
  - https://github.com/beartype/beartype

---

- DONE support msgpack in serialisation
- DONE Add mesh visual with hidden faces
- DONE issue with serialisation: currently camera is not serialised
  - may require to have my own Camera class ... 
  - not required, i can serialize the parameters (including the matrices)
- FIXED MatplotlibRendererDelta fails on multi viewport
- DONE keep only MatplotlibRendererDelta
  - remove MatplotlibRenderer
- DONE serialisation doesnt conserve uuid, fix this
- DONE Add type checking with pyright in Makefile
- DONE check all examples
- DONE make image work in 3d in MatplotlibRendererDelta
- DONE implement 3d
  - https://github.com/rougier/matplotlib-3d/ <- YES
  - https://github.com/rougier/tiny-renderer/blob/master/bunny.py
- DONE implement network client/server over http
  - `./network/client.py` send a scene.json
  - `./network/server.py` receive a scene.json and render it and send back a png
- DONE multiple viewports
- DONE from/to file
