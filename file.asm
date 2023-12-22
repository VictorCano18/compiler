.text
.globl main
main:
move $fp $sp
move $t5 $sp
jal new_main
addiu $sp $sp -4
addiu $sp $sp -4
addiu $sp $sp -4
addiu $sp $sp -4
addiu $sp $sp -4
compare:
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
lw $a0 12($fp)
sw $a0 20($t5)
lw $a0 20($t5)
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 4($fp)
lw $t1 4($sp)
addiu $sp $sp 4
bgt $t1 $a0 true_branch
false_branch:
lw $a0 12($fp)
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 8($fp)
lw $t1 4($sp)
sub $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 20($t5)
b end_if
true_branch:
lw $a0 12($fp)
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 8($fp)
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
sw $a0 20($t5)
end_if:
lw $a0 20($t5)
sw $a0 12($fp)
lw $a0 12($fp)
lw $ra 4($sp)
addiu $sp $sp 20
lw $fp 0($sp)
jr $ra
new_main:
sw $fp 0($sp)
addiu $sp $sp -4
li $a0 5
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 4
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 2
sw $a0 0($sp)
addiu $sp $sp -4
jal compare
