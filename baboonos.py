"""
pavian():
    strana = <0 ,1>
    while True:
        turn.wait()
        ls[strana].wait(som_lano)
        turn.signal()

        mplex.wait()
        ruckuj_po_lane()
        mplex.signal()

        ls[strana].signal(som_lano)

        strana := (strana +1 ) % 2
"""