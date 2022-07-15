import time
import pygame
import numpy as np

COLOR_BG = (56, 124, 68)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_FIRE = (255,69,0)
COLOR_YELLOW = (255, 234, 0)
COLOR_ASH = (119,136,153)
NUMBER_OF_RUNS = 10

def submatrix( matrix, startRow, startCol, size):
    return matrix[startRow:startRow+size,startCol:startCol+size]

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    for row, col in np.ndindex(cells.shape):
        neighborhood = [[cells[row-1,col-1],cells[row,-1,col],cells[row-1,col+1]],
                        [cells[row,col-1],cells[row,col],cells[row,col+1]],
                        [cells[row+1,col-1],cells[row+1,col],cells[row+1,col+1]]]
        diag = np.array([[0.785,0,0.785],[0,0,0],[0.785,0,0.785]])
        adj = np.array([[0,1,0],[1,0,1],[0,1,0]])
        current = np.array([[0,0,0],[0,1,0],[0,0,0]])

        print(neighborhood)
        burned_area = np.multiply(neighborhood,current) + np.multiply(neighborhood,adj) + np.multiply(diag,neighborhood)
        #diag = cells[row+2, col+2] + cells[row+2, col-1] + cells[row-1, col+2] + cells[row-1, col-1]
        #burned_area = cells[row, col] + adj# + 0.785*diag

        if burned_area > 1:
            burned_area = 1

        cells[row, col] = burned_area

        color = COLOR_BG if cells[row, col] == 0 else COLOR_FIRE

        if cells[row, col] == 1:
            if with_progress:
                updated_cells[row, col] = -1
                color = COLOR_ASH

        if 0<cells[row, col]<0.5:
            if with_progress:
                color = COLOR_YELLOW

        if cells[row,col]>0.5 and cells[row,col] <1:
            if with_progress:
                color = COLOR_FIRE

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    for i in range(NUMBER_OF_RUNS):
        update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

            time.sleep(0.1)


if __name__ == '__main__':
    main()