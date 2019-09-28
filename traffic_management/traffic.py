class TrafficProperties(object):
    FLOW_FACTOR = 0.05 / 60  # flow per minute depending on population
    PRIORITY_BASE_DURATION = 1
    PRIORITY_EXT_DURATION = 0.5
    JUNCTION_FLOW = 180  # flow per minute through the junction
    ACCELERATION_TIME = 0.25  # time before reaching the nominal junction flow
    WAIT_FACTOR = 0.05  # 'frustration factor' due to waiting


