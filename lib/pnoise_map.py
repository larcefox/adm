from noise import pnoise2
import numpy as np
import matplotlib.pyplot as plt

class MapGen:
    def __init__(
        self,
        shape=(100, 100, 3),
        scale=100,
        octaves=10,
        persistence=0.5,
        lacunarity=3,
        seed=np.random.randint(0, 100),
        ) -> None:
        
        self.shape = shape
        self.scale = scale
        self.seed = seed
        self.repeatx = self.shape[0]
        self.repeaty = self.shape[1]
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.noise = np.zeros(self.shape)
    
    def map_gen(self) -> np.array:
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                for z in range(self.shape[2]):
                    match z:
                        # This place is braine fuck, I changed places in array insted chenging coords.
                        case 2:
                            self.noise[x][y][z] = x * 100
                        case 0:
                            self.noise[x][y][z] = y * 100
                        case _:
                            self.noise[x][y][z] = pnoise2(
                                x / self.scale,
                                y / self.scale,
                                octaves=self.octaves,
                                base=self.seed,
                                repeatx=self.repeatx,
                                repeaty=self.repeaty,
                                persistence=self.persistence,
                                lacunarity=self.lacunarity,                                   
                                )  * 3000
        return self.noise.tolist()

if __name__ == '__main__':
    noise_map = MapGen()
    print(noise_map.map_gen())
    
