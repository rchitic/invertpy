from scipy.spatial.transform import Rotation as R

import numpy as np


class Sensor(object):
    def __init__(self, nb_input, nb_output, xyz=None, ori: R = None, noise=0., dtype='float32', name="sensor"):
        self._nb_input = nb_input
        self._nb_output = nb_output
        self._xyz = xyz if xyz is not None else np.zeros(3, dtype=dtype)
        self._ori = ori if ori is not None else R.from_euler('z', 0, degrees=False)
        self.noise = noise
        self.dtype = dtype

        self.name = name

    def reset(self):
        raise NotImplementedError()

    def _sense(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        callback = kwargs.pop('callback', None)
        out = self._sense(*args, **kwargs)

        if callback is not None:
            callback(self)

        return out

    def __repr__(self):
        return "Sensor(in=%d, out=%d, pos=(%.2f, %.2f, %.2f), ori=(%.2f, %.2f, %.2f), name='%s')" % (
            self._nb_input, self._nb_output,
            self.x, self.y, self.z,
            self.yaw_deg, self.pitch_deg, self.roll_deg, self.name
        )

    @property
    def xyz(self):
        return self._xyz

    @property
    def x(self):
        return self._xyz[0]

    @property
    def y(self):
        return self._xyz[1]

    @property
    def z(self):
        return self._xyz[2]

    @property
    def ori(self):
        return self._ori

    @property
    def euler(self):
        return self._ori.as_euler('ZYX', degrees=False)

    @property
    def yaw(self):
        return self.euler[0]

    @property
    def pitch(self):
        return self.euler[1]

    @property
    def roll(self):
        return self.euler[2]

    @property
    def euler_deg(self):
        return self._ori.as_euler('ZYX', degrees=True)

    @property
    def yaw_deg(self):
        return self.euler_deg[0]

    @property
    def pitch_deg(self):
        return self.euler_deg[1]

    @property
    def roll_deg(self):
        return self.euler_deg[2]

    @property
    def position(self):
        return self._xyz

    @property
    def orientation(self):
        return self._ori
