# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp import glm
from gsp import visual
from gsp.io.command import command
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color


class Volume(visual.Volume):

    __doc__ = visual.Volume.__doc__

    @command("visual.Volume")
    def __init__(
        self,
        volume_data: np.ndarray,
        point_size: float = 10.0,
        downsample_ratio: float = 1.0,
        alpha_factor: float = 1.0,
        jitter_position_factor: float = 0.0,
        remove_invisible_points_enabled: bool = True,
    ):
        volume_depth, volume_height, volume_width, color_ndim = volume_data.shape

        import time
        time_start = time.perf_counter()

        # sanity check - volume shape
        assert volume_depth > 0
        assert volume_height > 0
        assert volume_width > 0
        assert color_ndim == 4

        len_x = int(volume_width * downsample_ratio)
        len_y = int(volume_height * downsample_ratio)
        len_z = int(volume_depth * downsample_ratio)

        point_count = len_x * len_y * len_z

        # TODO should i sample that randomly - would be easier to vectorize
        positions = glm.vec3(point_count)
        fill_colors = glm.vec4(point_count)

        # positions[...] = np.random.uniform(-1, +1, (n, 3))
        # setup positions array to be a dense cube
        linspace_x = np.linspace(-1, 1, len_x)
        linspace_y = np.linspace(-1, 1, len_y)
        linspace_z = np.linspace(-1, 1, len_z)

        # TODO should be vectorized
        for index_x in range(len_x):
            for index_y in range(len_y):
                for index_z in range(len_z):
                    array_index = index_x * len_y * len_z + index_y * len_z + index_z
                    positions[array_index] = [
                        linspace_z[index_z],
                        linspace_y[index_y],
                        linspace_x[index_x],
                    ]
                    fill_colors[array_index] = volume_data[
                        int(index_z / downsample_ratio),
                        int(index_y / downsample_ratio),
                        int(index_x / downsample_ratio),
                    ]

        # multiply alpha (the forth dimension) of fill_colors
        fill_colors[..., 3] *= alpha_factor

        # optimisation: remove all positions and fill_colors where alpha is 0. it would be invisible anyways
        if remove_invisible_points_enabled:
            positions = positions[fill_colors[..., 3] > 0]
            fill_colors = fill_colors[fill_colors[..., 3] > 0]

        # Fake way to remove moire patterns
        positions += jitter_position_factor * np.random.normal(0, 1, positions.shape)

        time_elapsed = time.perf_counter() - time_start
        print(f"Volume initialization took {time_elapsed:.4f} seconds. length: {len(positions)}")
        
        super().__init__(
            positions=positions, sizes=point_size, fill_colors=fill_colors, __no_command__=True
        )

    def render(self, viewport=None, model=None, view=None, proj=None):

        super().render(viewport, model, view, proj)
        model = model if model is not None else self._model
        view = view if view is not None else self._view
        proj = proj if proj is not None else self._proj

        # Disable tracking for newly created glm.ndarray (or else,
        # this will create GSP buffers)
        tracker = glm.ndarray.tracked.__tracker_class__
        glm.ndarray.tracked.__tracker_class__ = None

        # Create the collection if necessary
        if viewport not in self._viewports:
            collection = viewport._axes.scatter([], [])
            collection.set_antialiaseds(True)
            collection.set_linewidths(0)
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect("resize_event", lambda event: self.render(viewport))

        # If render has been called without model/view/proj, we don't
        # render Such call is only used to declare that this visual is
        # to be rendered on that viewport.
        if self._transform is None:
            # Restore tracking
            glm.ndarray.tracked.__tracker_class__ = tracker
            return

        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1, 3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ self._transform.T)

        # Invert depth buffer values before sorting
        # This in place inversion is important for subsequent transforms
        positions[:, 2] = 1 - positions[:, 2]
        sort_indices = np.argsort(positions[:, 2])
        collection.set_offsets(positions[sort_indices, :2])
        self.set_variable("screen[positions]", positions)

        fill_colors = self.eval_variable("fill_colors")
        if isinstance(fill_colors, np.ndarray) and (len(fill_colors) == len(positions)):
            collection.set_facecolors(fill_colors[sort_indices])
        else:
            collection.set_facecolors(fill_colors)

        # line_colors = self.eval_variable("line_colors")
        # if isinstance(line_colors, np.ndarray) and (len(line_colors) == len(positions)):
        #     collection.set_edgecolors(line_colors[sort_indices])
        # else:
        #     collection.set_edgecolors(line_colors)

        # line_widths = self.eval_variable("line_widths")
        # if isinstance(line_widths, np.ndarray) and (len(line_widths) == len(positions)):
        #     collection.set_linewidths(line_widths[sort_indices])
        # else:
        #     collection.set_linewidths(line_widths)

        sizes = self.eval_variable("sizes")
        if isinstance(sizes, np.ndarray) and (len(sizes) == len(positions)):
            collection.set_sizes(sizes[sort_indices])
        else:
            collection.set_sizes([sizes] * len(positions))

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
