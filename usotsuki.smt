; 論理パズル①
(declare-const a Bool)
(declare-const b Bool)
(declare-const c Bool)

(assert (or 
  (and a (not b) (not c))
  (and (not a) b (not c))
  (and (not a) (not b) c)
))

(assert (and 
  (or a (not a))
  (or (and b (not a)) (and (not b) a))
  (or (and c (not b)) (and (not c) b))
))

(check-sat)
(get-model)