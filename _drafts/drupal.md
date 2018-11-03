-Deletar node baseado no tipo de conteúdo no Drupal 6
  <?php
    $node_type = 'article';
    $result = db_query("SELECT nid FROM {node} WHERE type='%s'",$node_type);
    while ($row = db_fetch_object($result))
    {
      set_time_limit(20);
      node_delete($row->nid);
      $deleted_count+=1;
    }
    drupal_set_message("$deleted_count nodes have been deleted");
  ?>

Desabilitar um módulo pelo banco de dados no Drupal 6:
 -mysql> UPDATE system SET status='0' WHERE name='views';

Trocar senha do usuário 1 pelo banco no Drupal 6: 
 -mysql> UPDATE {user} SET password = MD5('minhasenha') WHERE uid = 1 


