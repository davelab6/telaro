#!/usr/bin/clisp -C
;;;=============================================================================
;;; A Mark V. Shaney implementation in CLISP-flavored Common Lisp.
;;; Reads text or word pattern statistics on stdin until EOF, then prints
;;; Markov-chain text or word pattern statstics on stdout.
;;; Copyright (C) 2006 Darren Racine <dr@racinesystems.com>
;;;
;;; This program is free software; you can redistribute it and/or modify
;;; it under the terms of the GNU General Public License as published by
;;; the Free Software Foundation; either version 2 of the License, or
;;; (at your option) any later version.
;;;
;;; v1.0, 2006-10-22
;;;=============================================================================

;==<global vars & default values>==

(defparameter *order* 2)
(defparameter *input-type* 'text)
(defparameter *output-type* 'text)

;==<functions>==

(defun word-char-p (c)
  "Returns T if c is a non-whitespace character."
  (and (characterp c) (not (find c '(#\Space #\Tab #\Newline)))))

(defun getword (s &optional p)
  "Returns the next whitespace-delimited word from character stream 's'
  as a string. Returns nil when no words are left in the stream."
  (let ((c (read-char s nil)))
    (cond
      ((and (word-char-p p) (not (word-char-p c))) "")
      ((and (not (word-char-p c)) (not (null c))) (getword s))
      ((null c) nil)
      (t (string-concat (string c) (getword s c))))))

(defun buffer (item lst)
  "Return lst with first element dropped & item appended to the end."
  (append (cdr lst) (list item)))

(defun read-text ()
  "Read whitespace delimited words from stdin; compile and
  return word pattern statistics."
  (let ((stats nil)
        (queue (make-list (1+ *order*)))
        (s *standard-input*))
    (do ((word (getword s) (getword s))) ((null word) stats)
      (setq queue (buffer word queue))
      (let* ((wordlist (subseq queue 0 *order*))
             (follower (nth *order* queue))
             (stat-entry (find wordlist stats :key #'first :test #'equal)))
        (if stat-entry
          (let ((new-entry (append stat-entry `(,follower))))
            (setq stats
                  (cons new-entry (remove stat-entry stats :test #'equal))))
          (setq stats (cons `(,wordlist ,follower) stats)))))))

(defun write-text (stats wrote)
  "Write stochastic text to stdout based on the provided stats.
  'wrote' is a list of the most recently written words; should be
  (make-list *order*) at the top call."
  (let ((s (find wrote stats :key #'first :test #'equal)))
    (if (not s) (format t "~2%")
      (progn
        (setq wrote (buffer (nth (random (length (cdr s))) (cdr s)) wrote))
        (format t "~A " (nth (1- *order*) wrote))
        (write-text stats wrote)))))

(defun getnext (item l)
  "Return the element following the 1st occurrence of 'item' in list l."
  (cond
    ((null l) nil)
    ((equal item (car l)) (car (cdr l)))
    (t (getnext item (cdr l)))))

;==<main>==

; Parse command line args:
(if (find "-s" *args* :test #'equal) (setq *output-type* 'stats))
(if (find "-o" *args* :test #'equal)
  (let ((ovalue (getnext "-o" *args*)))
    (if (stringp ovalue)
      (setq ovalue (with-input-from-string (s ovalue) (read s))))
    (if (and (integerp ovalue) (> ovalue 0))
      (setq *order* ovalue)
      (progn
        (format t "~%markv: '~A' is not a valid value for the '-o' option~2%" ovalue)
        (exit 1)))))

; Seed the pseudorandom number generator:
(setq *random-state* (make-random-state t))

; Hackish input type detection!
(if (char= (peek-char nil *standard-input* nil) #\( )
  (setq *input-type* 'stats))

; Do what has been requested:
(cond
  ((and (eql *input-type* 'text) (eql *output-type* 'text))
   (write-text (read-text) (make-list *order*)))
  ((and (eql *input-type* 'text) (eql *output-type* 'stats))
   (prin1 (read-text)))
  ((and (eql *input-type* 'stats) (eql *output-type* 'text))
   (let ((stats (read *standard-input* nil)))
     (setq *order* (length (car (car stats))))
     (write-text stats (make-list *order*))))
  (t ;Both input & output are stats in this case
    (prin1 (read *standard-input* nil))))

