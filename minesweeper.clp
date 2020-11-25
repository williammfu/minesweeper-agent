;; minesweeper.clp
;; Rule based agent to solve a minesweeper instance
;; Opens tile at coordinates E(0,0)

;; (tile x y bombs cond.)
;; (tile x y flag)

(deftemplate tile
    (slot x)
    (slot y)
    (slot bombs)
    (slot state)
)

(deftemplate current-tile
    (slot x)
    (slot y)
)

(deftemplate closed-around
    (slot x)
    (slot y)
    (slot amount)
)

(deffunction is-pq-around-xy
    (?p ?q ?x ?y)
    (or
        (and (= ?p ?x) (= ?q (+ ?y 1)))
        (and (= ?p ?x) (= ?q (- ?y 1)))
        (and (= ?p (+ ?x 1)) (= ?q (+ ?y 1)))
        (and (= ?p (+ ?x 1)) (= ?q (- ?y 1))) 
        (and (= ?p (+ ?x 1)) (= ?q ?y ))
        (and (= ?p (- ?x 1)) (= ?q (+ ?y 1)))
        (and (= ?p (- ?x 1)) (= ?q ?y))
        (and (= ?p (- ?x 1)) (= ?q (- ?y 1))) 
    )
)

(deffunction in-range
    (?x ?y ?state ?lower-x ?upper-x ?lower-y ?upper-y)
    (and
        (eq ?state close)
        (and (>= ?x ?lower-x) (<= ?x ?upper-x))
        (and (>= ?y ?lower-y) (<= ?y ?upper-y))
    )
)

(defrule start-zero
    (declare (salience 100))
    ?f <- (tile (x 0) (y 0) (bombs ?bombs) (state close))
    =>
    (retract ?f)
    (assert (tile (x 0) (y 0) (bombs ?bombs) (state open)))
)

;; Opens all tiles surrounding tile E(x,y) with E(x,y) = 0
(defrule spread
    (declare (salience 1))
    (tile (x ?x) (y ?y) (bombs 0) (state open))
    ?f <- (tile (x ?p) (y ?q) (bombs ?value2) (state close)) ;; Yang mau di buka
    (test (is-pq-around-xy ?p ?q ?x ?y))
    =>
    ; (printout t "Tile open at (" ?p "," ?q ")" crlf)
    (retract ?f)
    (assert (tile (x ?p) (y ?q) (bombs ?value2) (state open)))
) 

;; Menghitung tile yang tertutup di sekitar E(x,y)
;; Boleh di-assert kalo mau
(defrule count-closed-around-tile
    (tile (x ?x) (y ?y) (bombs ?bombs) (state open))
    (test (> ?bombs 0))
    =>
    ;; TO DO assert here
    (bind ?count (length$ (find-all-facts ((?g tile)) (in-range ?g:x ?g:y ?g:state (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))))
    (assert (closed-around (x ?x) (y ?y) (amount ?count)))
    (printout t "Amount closed around  (" ?x "," ?y ") = ")
    (printout t (length$ (find-all-facts ((?g tile)) (in-range ?g:x ?g:y ?g:state (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))) crlf)
)

;; [BELUM KELAR]
; (defrule create-flag
;     ?f <- (tile (x ?x) (y ?y) (bombs ?bombs) (state close))
;     (closed-around (x ?x) (y ?x) (amount ?amount))
;     (test (= ?amount ?))
;     =>
;     (retract ?f)
;     (assert (tile (x ?x) (y ?y) (bombs -1) (state close)))
; )

; (defrule click-bomb-safe
;     ?f <- (tile (x ?x) (y ?y) (bombs ?bombs) (state close))
;     (test (> ?bombs -1))
; =>
;     (retract ?f)
;     (printout t "bomb safe" crlf)
;     ; (printout t "(" ?x " , "  ?y ") safe. Open." crlf)
;     (assert (tile (x ?x) (y ?y) (bombs ?bombs) (state open))) 
    
; )

; (defrule click_bomb_exit
;     ?f <- (tile (x ?x) (y ?y) (bombs ?bombs) (state close))
;     (test (= ?bombs -1))
; =>
;     (retract ?f)
;     (printout t "(" ?x " , "  ?y ") is not safe. Bomb. Duar." crlf)  
;     ; (exit)
; )








