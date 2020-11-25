(deftemplate  observations (multislot breeze) (multislot stench))
 
(deffacts initial-states 
    (xpositions 1 2 3 4) 
    (ypositions 1 2 3 4) 
    (observations (breeze 2 1))
    (observations (breeze 2 3))
    (observations (breeze 3 2)) 
    (observations (breeze 3 4)) 
    (observations (breeze 4 1)) 
    (observations (breeze 4 3))
    (observations (stench 1 2))
    (observations (stench 1 4)) 
    (observations (stench 2 3))
)

(defrule new-positions
    (xpositions $?xpos)
    (ypositions $?ypos)
=>
    (assert (new-xpositions nil ?xpos nil))
    (assert (new-ypositions nil ?ypos nil))
)

(defrule detect-pit
    (new-xpositions $? ?ax ?x ?bx $?)
    (new-ypositions $? ?ay ?y ?by $?)
    (or (observations (breeze ?x ?by)) (test (eq ?by nil)))
    (or (observations (breeze ?ax ?y)) (test (eq ?ax nil)))
    (or (observations (breeze ?x ?ay)) (test (eq ?ay nil)))
    (or (observations (breeze ?bx ?y)) (test (eq ?bx nil)))
=>
    (assert (PitT ?x ?y))
    (printout t "(" ?x " , "  ?y ") Pit" crlf)  
)

(defrule detect-wumpus
    (new-xpositions $? ?ax ?x ?bx $?)
    (new-ypositions $? ?ay ?y ?by $?)
    (or (observations (stench ?x ?by)) (test (eq ?by nil)))
    (or (observations (stench ?ax ?y)) (test (eq ?ax nil)))
    (or (observations (stench ?x ?ay)) (test (eq ?ay nil)))
    (or (observations (stench ?bx ?y)) (test (eq ?bx nil)))
=>
    (assert (WumpusT ?x ?y))
    (printout t "(" ?x " , "  ?y ") Wumpus" crlf)  
)

(defrule noPitWumpus
    (xpositions $? ?x $?)
    (ypositions $? ?y $?)
    (not (PitT ?x ?y))
    (not (WumpusT ?x ?y))
=>
    (printout t "(" ?x " , "  ?y ") Safe" crlf)  
)