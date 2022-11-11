import mesa
from modelo_limpieza import *

GRID_WIDTH = 15
GRID_HEIGHT = 15

NUM_AGENTS = 8

TRASH_PERCENTAJE = 50

MAX_STEPS = 200


def agent_portrayal(agent):
    if isinstance(agent, AgenteBasura):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Color": "rgb(146, 90, 55)",
                     "r": 0.4,
                     "Layer": 0}
        if agent.cleaned:
            portrayal["Color"] = "rgba(146, 90, 55, 0.1)"
        return portrayal
    else:
        return {"Shape": "rect",
                "Filled": "true",
                "Color": "rgb(223, 190, 44)",
                "w": 0.6,
                "h": 0.6,
                "Layer": 1}


grid = mesa.visualization.CanvasGrid(
    agent_portrayal, GRID_WIDTH, GRID_HEIGHT, 500, 500)


chart = mesa.visualization.ChartModule([{"Label": "Total agent steps",
                                         "Color": "Black"}],
                                       data_collector_name='datacollector')

chart2 = mesa.visualization.ChartModule([{"Label": "Clean cells percentaje",
                                         "Color": "Blue"}],
                                        data_collector_name='datacollector')


server = mesa.visualization.ModularServer(
    ModeloLimpieza, [grid, chart, chart2], "Robot de limpieza", {
        "width": GRID_WIDTH,
        "height": GRID_HEIGHT,
        "N": NUM_AGENTS,
        "percentaje": TRASH_PERCENTAJE,
        "max_steps": MAX_STEPS}
)
server.port = 8521  # The default
server.launch()
