Game
  @homepage
  g.state = start
    botton -> start
      if pressed -> g.state = game
    option -> nothingbuttroll

  @game
  g.state = game
        player
        spawn = lower
        out of state 
            move
            pick torpedo/first-aid-kit
        state normal
            shooting (bullet)(normal speed)
            shooting (torpedo)
            get hurt
                state hurt
                    visible (flash 1~1.5sec)
                    shooting(bullet)(lower speed)
                    shooting(torpedo)(disable)
            get frist-aid-kit
                state heal
                    flash -> (normal ~ Green 1 time)
        
        Enemy - solider
            
            out of state
            shooting = bullet(normal speed)
            state alive
            left-right move(20~30pixel) 
            number limit
            get hurt
            state dead
            random spawn tropedo/first-aid-kit 
            relive 1
            go back to where it dead 
            
        Enemy - Boss
            out of state
            left-right move(20~30pixel)
            state alive
            shooting = bullet(normal speed)
            target -> player
            random spwan tropedo
            health < 50%
                state mad 
                    shooting = bullet(faster speed)
                    state rush
                    bump into player (cause 5 times damage)

@score
    player's health <0
      g.state = lose
        botton -> return
          g.state = start

    boss' health <0
      g.state = win 
        botton -> return
          g.state = start              
