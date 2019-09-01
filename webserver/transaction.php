<?php
function randw($length=10){
        return substr(str_shuffle("qwertyuiopasdfghjklzxcvbnm"),0,$length);
    }


$from = htmlspecialchars($_POST['from']);
$to = htmlspecialchars($_POST['to']);
$amount = htmlspecialchars($_POST['amount']);

$word1 = randw();
$word2 = randw();
$startby = rand(1000,9999);

$transaction = '{"from":"' . $from . '","to":"' . $to . '","amount":' . $amount . ',"proof-of-work-word1":"' . $word1 . '","proof-of-work-word2":"' . $word2 . '","proof-of-work-startby":"' . $startby . '"}';

$handle = fopen('mine', 'a');
fwrite($handle, $transaction . "\n");
fclose($handle);
?>