#!/usr/bin/python3
# encoding=utf-8

"""
                         _____  _____  _____  _____  _____         _____
           /////  /     /____/ /___ / /___ / /_ __/ /_ __/ /|  // /____/
           ////  //    //___  //__// //__//   //     //   / | // //___
          ////  //    // \ / / ___/ /___ /   //     //   //||// // \ /
          ///  ///   //__// //\\   //  //   //   __//_  // | / //__//
         ///  ///   /____/ //  \\ //  //   //   /____/ //  |/ /____/
         //  ////      _   _   _   _   _  _ _  _   _  _ _  __  __
        //  ////  |   |_| |_) / \ |_) |_|  |  / \ |_)  |  |_  (_
        /  /////  |__ | | |_) \_/ | \ | |  |  \_/ | \ _|_ |__ __)
    =================================================================
      Grating Science SVIP (Staged Visualized Integrated Platform)
"""

import pygame
from pygame.locals import *

from scenes import Welcome


def main():
    pygame.init()
    pygame.display.set_mode((1920, 1080), FULLSCREEN)
    # pygame.display.set_mode((1920, 1080))
    surface = pygame.display.get_surface()
    font = 'font/wqy-microhei.ttc'
    fps = 60
    clock = pygame.time.Clock()
    scene = Welcome(surface, font)
    while True:
        scene = scene.tick()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
