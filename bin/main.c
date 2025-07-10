
int check_neighbours(int SIZE,int grid[SIZE][SIZE], int x, int y) {
    int count = 0;
    count = grid[x - 1][y - 1]+grid[x - 1][y]+grid[x - 1][y + 1]+grid[x][y - 1]+grid[x][y + 1]+grid[x + 1][y - 1]+grid[x + 1][y]+grid[x + 1][y + 1];
}