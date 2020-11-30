;; minesweeper.clp
;; Rule based agent to solve a minesweeper instance

;; Representasi board size x size
(deftemplate board
    (slot size)
    (slot total-mines)
)  

;; Representasi tile pada board 
;; bombs <-- banyaknya bomb di sekitar tile
;; state <-- open, close, flagged
(deftemplate tile
    (slot x)
    (slot y)
    (slot bombs)
    (slot state)
)

;; Banyaknya tile yang tertutup (state close) berada di sekitar E(x,y)
(deftemplate closed-around
    (slot x)
    (slot y)
    (slot amount)
)

;; tile(p,q) adalah tile tertutup (state close) dan berada di sekitar E(x,y)
(deftemplate closed-around-tile
    (slot x)
    (slot y)
    (multislot tile)
)

;; Banyaknya tile yang udah di flag (state flag) di sekitar E(x,y)
(deftemplate flag-around
    (slot x)
    (slot y)
    (slot num)
)

;; Untuk kepentingan mencoba tiles
(deftemplate opened-safe
    (slot x-open)
    (slot y-open)
)

;; Silahkan un-comment untuk menguji program
; (deffacts fakta
;     (board (size 5) (total-mines 2))
;     (tile (x 0) (y 0) (bombs 0) (state close))
;     (tile (x 0) (y 1) (bombs 0) (state close))
;     (tile (x 0) (y 2) (bombs 0) (state close))
;     (tile (x 0) (y 3) (bombs 0) (state close))
;     (tile (x 0) (y 4) (bombs 0) (state close))
;     (tile (x 1) (y 0) (bombs 0) (state close))
;     (tile (x 1) (y 1) (bombs 0) (state close))
;     (tile (x 1) (y 2) (bombs 1) (state close))
;     (tile (x 1) (y 3) (bombs 1) (state close))
;     (tile (x 1) (y 4) (bombs 1) (state close))
;     (tile (x 2) (y 0) (bombs 0) (state close))
;     (tile (x 2) (y 1) (bombs 0) (state close))
;     (tile (x 2) (y 2) (bombs 1) (state close))
;     (tile (x 2) (y 3) (bombs -1) (state close))
;     (tile (x 2) (y 4) (bombs 1) (state close))
;     (tile (x 3) (y 0) (bombs 0) (state close))
;     (tile (x 3) (y 1) (bombs 0) (state close))
;     (tile (x 3) (y 2) (bombs 1) (state close))
;     (tile (x 3) (y 3) (bombs 2) (state close))
;     (tile (x 3) (y 4) (bombs 2) (state close))
;     (tile (x 4) (y 0) (bombs 0) (state close))
;     (tile (x 4) (y 1) (bombs 0) (state close))
;     (tile (x 4) (y 2) (bombs 0) (state close))
;     (tile (x 4) (y 3) (bombs 1) (state close))
;     (tile (x 4) (y 4) (bombs -1) (state close))
; )

;; Mengembalikan true jika E(x,y) berada dalam keadaan tertutup
;; dan sesuai dengan range yang ada
(deffunction in-range
    (?x ?y ?state ?lower-x ?upper-x ?lower-y ?upper-y)
    (and
        (eq ?state close)
        (and (>= ?x ?lower-x) (<= ?x ?upper-x))
        (and (>= ?y ?lower-y) (<= ?y ?upper-y))
    )
)

;; Mengembalikan true jika E(x,y) adalah bomb (state flagged)
;; dan sesuai dengan range yang ada
(deffunction in-range-flag
    (?x ?y ?state ?lower-x ?upper-x ?lower-y ?upper-y)
    (and
        (eq ?state flagged)
        (and (>= ?x ?lower-x) (<= ?x ?upper-x))
        (and (>= ?y ?lower-y) (<= ?y ?upper-y))
    )
)

;; Memulai permainan dengan membuka E(0,0)
(defrule start-zero
    (declare (salience 100))
    ?f <- (tile (x 0) (y 0) (bombs ?bombs) (state close))
    =>
    (modify ?f (state open))
)

;; Membuka semua tile yang mengelilingi (x,y) dengan E(x,y) = 0
(defrule spread
    (declare (salience 10))
    (tile (x ?x) (y ?y) (bombs 0) (state open))
    ?f <- (tile (x ?p) (y ?q) (bombs ?value2) (state close)) ;; Yang mau di buka
    (test (in-range ?p ?q close (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))
    =>
    (printout t "Spread Open (" ?p "," ?q ")" crlf)
    (modify ?f (state open))
) 

;; Menghitung tile yang tertutup di sekitar (x,y)
(defrule count-closed-around-tile
    (declare (salience 1))
    (tile (x ?x) (y ?y) (bombs ?bombs) (state open))
    ; ?f <- (flag-around (x ?x) (y ?y) (num ?num))
    (test (> ?bombs 0))
    =>
    (bind ?count (length$ (find-all-facts ((?g tile)) (in-range ?g:x ?g:y ?g:state (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))))
    (do-for-all-facts ((?f flag-around)) (and (= ?f:x ?x) (= ?f:y ?y)) 
        (modify ?f (num (length$ (find-all-facts ((?g tile)) (in-range-flag ?g:x ?g:y ?g:state (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1))))))
    )
    ; (bind ?count-flag (length$ (find-all-facts ((?g tile)) (in-range-flag ?g:x ?g:y ?g:state (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))))
    ; (modify ?f (num ?count-flag))
    (assert (closed-around (x ?x) (y ?y) (amount ?count)))
    (printout t "count-closed-around-tile (" ?x "," ?y ") = " ?count crlf)
    ; (printout t "Amount closed around (" ?x "," ?y ") = " ?count " flag:" ?num crlf)
)

;; Menambahkan koordinat tile yang tertutup di sekitar (x,y)
(defrule set-closed-around-tile
    (declare (salience 1))
    (tile (x ?x) (y ?y) (bombs ?bombs1) (state open))
    (tile (x ?p) (y ?q) (bombs ?bombs2) (state close))
    (closed-around (x ?x) (y ?y) (amount ?amount))
    (test (> ?amount 0))
    (test (> ?bombs1 0))
    (test (in-range ?p ?q close (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))
    =>
    ; (printout t "closed-around-tile (" ?x "," ?y ") (tile " ?p " " ?q ")" crlf)
    (assert (closed-around-tile (x ?x) (y ?y) (tile ?p ?q)))
)

;; Membuka tile (x,y) jika dinilai sudah aman
(defrule open-bomb-safe
    (tile (x ?x) (y ?y) (bombs ?bombs) (state open)) 
    ?g <- (tile (x ?x1) (y ?y1) (bombs ?bombs1) (state close))
    ?h <- (closed-around-tile (x ?x) (y ?y) (tile ?x1 ?y1))
    (flag-around (x ?x) (y ?y) (num ?num))
    ?flag <- (flag-around (x ?x1) (y ?y1) (num ?numflag))
    (test (!= ?bombs 0))
    (test (= ?bombs ?num))
    =>
    (modify ?g (state open))
    (printout t "Open bomb safe (" ?x1 "," ?y1 ") : Patokan (" ?x "," ?y ")" crlf)
    (bind ?count (length$ (find-all-facts ((?g tile)) (in-range ?g:x ?g:y ?g:state (- ?x1 1) (+ ?x1 1) (- ?y1 1) (+ ?y1 1)))))
    (bind ?count-flag (length$ (find-all-facts ((?g tile)) (in-range-flag ?g:x ?g:y ?g:state (- ?x1 1) (+ ?x1 1) (- ?y1 1) (+ ?y1 1)))))
    (modify ?flag (num ?count-flag))
    ; (printout t "OPEN" ?x1 " " ?y1 " : " ?count-flag " " ?count crlf)
    (assert (closed-around (x ?x1) (y ?y1) (amount ?count)))
    (assert (opened-safe (x-open ?x1) (y-open ?y1)))
    (retract ?h)
    ; (printout t ?num crlf)
)

;; Membuat flag pada (p,q)
(defrule create-flag
    (declare (salience -1))
    
    (tile (x ?x) (y ?y) (bombs ?bombs1) (state open)) ;; E(x,y) adalah tile pusat yang diteliti
    (closed-around (x ?x) (y ?y) (amount ?amount)) ;; Jumlah tile tertutup di sekitar E(x,y)
    (flag-around (x ?x) (y ?y) (num ?num)) ;; Jumlah flag di sekitar E(x,y)
    ?t2 <- (tile (x ?p) (y ?q) (bombs ?bombs2) (state close)) ;; E(p,q) adalah tile yang tertutup
    ?board <- (board (size ?size) (total-mines ?total)) ;; Keadaan board saat ini
    
    (test (= ?bombs1 (+ ?amount ?num))) ;; jumlah kosong == jumlah bom (artinya disekitarnya semua bom)
    (test (in-range ?p ?q close (- ?x 1) (+ ?x 1) (- ?y 1) (+ ?y 1)))
    (test (> ?total 0)) ;; Pastikan jumlah mines pada board tidak negatif
    =>
    (printout t "create-flag at (" ?p "," ?q ") by (" ?x "," ?y ")" crlf)
    (modify ?t2 (state flagged))
    (modify ?board (total-mines (- ?total 1))) ;; Jumlah bomb yang belum diketahui berkurang satu
)

;; Mengupdate jumlah bomb di sekitar tile (x1, y1) yang baru saja di flag
(defrule after-flag
    (declare (salience 2))
    (tile (x ?x1) (y ?y1) (bombs ?bombs) (state flagged))
    ?f <- (closed-around-tile (x ?x2) (y ?y2) (tile ?x1 ?y1))
    ?g <- (flag-around (x ?x2) (y ?y2) (num ?num))
    ?h <- (closed-around (x ?x2) (y ?y2) (amount ?amount))
    =>
    (printout t "Flagged(" ?x1 "," ?y1") --> (" ?x2 "," ?y2 ") Flag=" (+ ?num 1) " Closed around=" (- ?amount 1) crlf)
    (retract ?f)
    (modify ?g (num (+ ?num 1)))
    (modify ?h (amount (- ?amount 1)))
)

;; Print state semua tile
(defrule print-all
    (declare (salience -10))
    (board (total-mines 0))
    (tile (x ?x) (y ?y) (state flagged))
    =>
    (printout t "Flagged(" ?x "," ?y ")" crlf)
)

;; Updating closed-around value around tile E(x1, y1)
;; which have just opened
(defrule retract-closed-around
    ; (declare (salience 1))
    (tile (x ?x1) (y ?y1) (bombs ?bombs) (state open))
    ?f <- (closed-around-tile (x ?x2) (y ?y2) (tile ?x1 ?y1))
    ?g <- (closed-around (x ?x2) (y ?y2) (amount ?amount))
    ; (tile (x ?x1) (y ?y1) (state open))
    =>
    (printout t "Tarik (" ?x1 "," ?y1 ") dari (" ?x2 "," ?y2 ")" crlf)
    (modify ?g (amount (- ?amount 1)))
    (retract ?f)
)