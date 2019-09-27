class TrafficProperties(object):
    FLOW_FACTOR = 0.05 / 60  # flow per minute depending on population
    PRIORITY_BASE_DURATION = 1
    PRIORITY_EXT_DURATION = 0.5
    JUNCTION_FLOW = 200  # flow per minute through the junction

    @staticmethod
    def get_outflow(time):
        return int(TrafficProperties.JUNCTION_FLOW * time)

    @staticmethod
    def get_base_outflow():
        return TrafficProperties.get_outflow(TrafficProperties.PRIORITY_BASE_DURATION)

    @staticmethod
    def get_ext_outflow():
        return TrafficProperties.get_outflow(TrafficProperties.PRIORITY_EXT_DURATION)


