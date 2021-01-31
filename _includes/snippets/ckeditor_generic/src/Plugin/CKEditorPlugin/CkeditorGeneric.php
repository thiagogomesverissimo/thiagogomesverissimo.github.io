<?php

namespace Drupal\ckeditor_generic\Plugin\CKEditorPlugin;

use Drupal\ckeditor\CKEditorPluginBase;
use Drupal\editor\Entity\Editor;


/**
 * Defines the "ckeditor_generic" plugin.
 *
 * @CKEditorPlugin(
 *   id = "ckeditor_generic",
 *   label = @Translation("CKEditor Button")
 * )
 */
class CkeditorGeneric extends CKEditorPluginBase {

  /**
   * {@inheritdoc}
   */
  public function getFile() {
    return drupal_get_path('module', 'ckeditor_generic') . '/js/plugin.js';
  }

  /**
   * {@inheritdoc}
   */
  public function getConfig(Editor $editor) {
    return array(
      'dialog_title_insert' => $this->t('Insert a Text'),
    );
  }

  /**
   * Implements CKEditorPluginButtonsInterface::getButtons().
   */
  public function getButtons() {
    return array(
      'ckeditor_generic_button' => array(
        'label' => $this->t('Ckediton Button'),
        'image' => drupal_get_path('module', 'ckeditor_generic') . '/images/icone.png',
      ),
    );
  }

}