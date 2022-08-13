from src import RandomWalk


if __name__ == '__main__':
    r = RandomWalk('/Users/liammccann/Documents/git_repositories/reinforcement-learner/tracks/L-track.txt')
    r.run()
    print(r.loss)
