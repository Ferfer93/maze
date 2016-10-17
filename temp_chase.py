        if _ping_response is not None:
            self.last_ping_response = _ping_response
            self.turns_since_ping = 0
            for player in self.last_ping_response:
                posB = None
                posG = None
                if isinstance(player,Baddy):
                    posB = self.last_ping_response[player]
                else:
                    posG = self.last_ping_response[player]
                self.next_ping = min([int(0.5*sqrt(posB[0]**2+posB[1]**2)),int(0.5*sqrt(posG[0]**2+posG[1]**2))])
                self.last_BG_pos = posB - posG
        else:
            self.next_ping -= 1
            for player in self.last_ping_response:
                if isinstance(player,Goody):
                    self.last_G_pos = self.last_ping_response[player]
                else:
                    self.last_B_pos = self.last_ping_response[player]
                    
        if self.next_ping == 0:
            return PING
        else:
            if posB[0]**2 + posB[1]**2 > posG[0]**2 + posG[1]**2:
                diag_G_x = last_G_pos[0] + last_G_pos[1]
                diag_G_y = last_G_pos[0] - last_G_pos[1]
                if diag_G_x > 0 and diag_G_y < 0:
                    if not obstruction[UP]:
                        return UP
                    else:
                        if np.randint(0,2) == 0:
                            if not obstruction[LEFT]:
                                return LEFT
                            elif not obstruction[RIGHT]:
                                return RIGHT
                        else:
                            if not obstruction[RIGHT]:
                                return RIGHT
                            elif not obstruction[LEFT]:
                                return LEFT
                        return STAY
                elif diag_G_x > 0 and diag_G_y > 0:
                    #G is right
                    if not obstruction[RIGHT]:
                        return RIGHT
                    else:
                        if np.randint(0,2) == 0:
                            if not obstruction[UP]:
                                return UP
                            elif not obstruction[DOWN]:
                                return DOWN
                        else:
                            if not obstruction[DOWN]:
                                return DOWN
                            elif not obstruction[UP]:
                                return UP
                        return STAY
                elif diag_G_x < 0 and diag_G_y > 0:
                    #G is down
                    if not obstruction[DOWN]:
                        return DOWN
                    else:
                        if np.randint(0,2) == 0:
                            if not obstruction[LEFT]:
                                return LEFT
                            elif not obstruction[RIGHT]:
                                return RIGHT
                        else:
                            if not obstruction[RIGHT]:
                                return RIGHT
                            elif not obstruction[LEFT]:
                                return LEFT
                        return STAY
                elif diag_G_x < 0 and diag_G_y < 0:
                    #G is left
                    if not obstruction[LEFT]:
                        return LEFT
                    else:
                        if np.randint(0,2) == 0:
                            if not obstruction[UP]:
                                return UP
                            elif not obstruction[DOWN]:
                                return DOWN
                        else:
                            if not obstruction[DOWN]:
                                return DOWN
                            elif not obstruction[UP]:
                                return UP
                        return STAY