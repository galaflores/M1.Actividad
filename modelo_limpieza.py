import mesa
import random


class AgenteLimpieza(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        if len(possible_steps) < 8:
            for _ in range(8 - len(possible_steps)):
                possible_steps.append(None)

        new_position = self.random.choice(possible_steps)
        if new_position is not None:
            self.model.grid.move_agent(self, new_position)
            self.model.total_agent_steps += 1

    def vacuum(self, agent):
        agent.cleaned = True
        self.model.trash_count -= 1

        clean_cells = self.model.num_cells - self.model.trash_count
        self.model.clean_cells_percentaje = (
            clean_cells * 100 / self.model.num_cells)

    def step(self):
        pos_x = self.pos[0]
        pos_y = self.pos[1]
        cell_content = self.model.grid.grid[pos_x][pos_y]
        for agent in cell_content:
            if isinstance(agent, AgenteBasura) and not agent.cleaned:
                self.vacuum(agent)
            else:
                self.move()
                break


class AgenteBasura(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned = False

    def step(self):
        pass


class ModeloLimpieza(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, width, height, N, percentaje, max_steps):
        self.num_cells = width * height

        self.max_steps = max_steps
        self.num_agents = N

        self.trash_count = 0
        self.clean_cells_percentaje = 0
        self.total_agent_steps = 0
        self.final_cleaning_time = 0

        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)

        id = 0
        # Create cleaning agents
        for _ in range(self.num_agents):
            a = AgenteLimpieza(id, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (1, 1))
            id += 1

        # Create trash agents
        for iy in range(height):
            for jx in range(width):
                if random.random() <= percentaje / 100:
                    ta = AgenteBasura(id, self)
                    self.grid.place_agent(ta, (jx, iy))
                    id += 1
                    self.trash_count += 1

        self.clean_cells_percentaje = (
            self.num_cells - self.trash_count) * 100 / self.num_cells

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total agent steps": "total_agent_steps",
                "Clean cells percentaje": "clean_cells_percentaje"})

    def step(self):
        if self.schedule.steps < self.max_steps and self.trash_count > 0:
            self.schedule.step()
            self.datacollector.collect(self)
        else:
            if not self.final_cleaning_time:
                self.final_cleaning_time = self.schedule.steps
                self.print_data()

            self.running = False

    def print_data(self):
        print("Final cleaning time: ", self.final_cleaning_time)
        print("Total agent steps: ", self.total_agent_steps)
        print(f"Cleaning cell percentaje: {self.clean_cells_percentaje:.2f}%")
