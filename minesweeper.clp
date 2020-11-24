;; minesweeper.clp
;; Rule based agent to solve a minesweeper instance

;; Opens tile at coordinates E(0,0)
(defrule start-zero
    (declare (salience 100))
    ?f <- (tile 0 0 ?bombs close)
    =>
    (retract ?f)
    (assert (tile 0 0 ?bombs open))
)

;; [BELUM KELAR]
;; Opens all tiles with E(x,y) = 0
(defrule spread
    (tile ?x ?y 0 open)
    (tile ?p ?q ?bombs close)
    (test (= ?x ?p) | (= ?x))
    =>
    (assert (tile ?p ?q ?bombs open))
)