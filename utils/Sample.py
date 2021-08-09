class Sample:
    def __init__(self, sample_height=0, data_points=[]):
        self.sample_height = sample_height
        self.data_points = data_points

    def append_data_point(self, data_point):
        self.data_points.append(data_point)
