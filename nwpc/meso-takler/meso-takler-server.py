import os
import takler


class TestServer(object):
    def __init__(self):
        self.server = takler.Server()
        self.bunch = self.server.bunch

        self.grapes_meso_suite = self.bunch.add_suite("meso")
        self.grapes_meso_suite.var_map["suite_home"] = os.path.join(os.path.dirname(__file__), '..')
        self.pre_data = self.grapes_meso_suite.append_child("pre_data")
        self.bckg = self.pre_data.append_child("bckg")
        self.t639_grib2bin = self.bckg.append_child("t639_grib2bin")
        self.obs = self.pre_data.append_child("obs")
        self.obs_proc = self.obs.append_child("obs_proc")


def main():
    # add suite
    test_server = TestServer()
    test_server.server.run_server()


if __name__ == "__main__":
    main()
