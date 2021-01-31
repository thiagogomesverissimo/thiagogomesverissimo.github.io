---
title: 'Módulo ckeditor drupal'
date: 2021-01-26
permalink: /posts/modulo-ckeditor-drupal
categories:
  - tutorial
tags:
  - drupal
---

As vezes é muito útil injetar um botão nosso no ckeditor do Drupal,
segue-se um exemplo de um botão customizado ao ser clicado abre um modal com ajax
que recebe um texto e o injeta no corpo do texto. Isso em si não é nada útil,
mas a possibilidade de interceptamos e fazermos qualquer modificação com esse botão.

Criando um módulo chamado ckeditor_generic com ckeditor_generic.info.yml:
{% highlight yml %}
{% include ckeditor_generic/ckeditor_generic.info.yml %}
{% endhighlight %}

O plugin que implementa `CKEditorPluginBase` colocamos em src/Plugin/CKEditorPlugin/CkeditorGeneric.php:
{% highlight php %}
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
{% endhighlight %}
em /images/icone.png coloque uma imagem qualquer para o ícone do seu botão e
crie `/js/plugin.js` por enquanto vazio.

Agora criemos um arquivo para o formulário em src/Form/CkeditorGenericDialog.php:
{% highlight php %}
<?php

namespace Drupal\ckeditor_generic\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\filter\Entity\FilterFormat;
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\HtmlCommand;
use Drupal\editor\Ajax\EditorDialogSave;
use Drupal\Core\Ajax\CloseModalDialogCommand;

class CkeditorGenericDialog extends FormBase {

  /**
   * {@inheritdoc}
   */
  public function getFormId() {
    return 'editor_ckeditor_generic_dialog';
  }

  /**
   * {@inheritdoc}
   *
   * @param \Drupal\filter\Entity\FilterFormat $filter_format
   *   The filter format for which this dialog corresponds.
   */
  public function buildForm(array $form, FormStateInterface $form_state, FilterFormat $filter_format = NULL) {

    $user_input = $form_state->getUserInput();
    $input = isset($user_input['editor_object']) ? $user_input['editor_object'] : array();

    $form['#tree'] = TRUE;
    $form['#attached']['library'][] = 'editor/drupal.editor.dialog';
    $form['#attached']['library'][] = 'ckeditor_generic/ckeditor_generic.dialog';

    $form['#prefix'] = '<div id="editor-ckeditor-generic-dialog-form">';
    $form['#suffix'] = '</div>';

    $form['attributes']['body'] = array(
      '#type' => 'textarea',
      '#title' => $this->t('Body'),
      '#default_value' => isset($input['body']) ? $input['body'] : '',
      '#size' => 50,
    );

    $form['actions'] = array(
      '#type' => 'actions',
    );
    $form['actions']['save_modal'] = array(
      '#type' => 'submit',
      '#value' => $this->t('Insert'),
      // No regular submit-handler. This form only works via JavaScript.
      '#submit' => array(),
      '#ajax' => array(
        'callback' => '::submitForm',
        'event' => 'click',
      ),
    );

    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {
    $response = new AjaxResponse();

    if ($form_state->getErrors()) {
      unset($form['#prefix'], $form['#suffix']);
      $form['status_messages'] = [
        '#type' => 'status_messages',
        '#weight' => -10,
      ];
      $response->addCommand(new HtmlCommand('#editor-ckeditor-generic-dialog-form', $form));
    }
    else {
      $response->addCommand(new EditorDialogSave($form_state->getValues()));
      $response->addCommand(new CloseModalDialogCommand());
    }

    return $response;
  }

}
{% endhighlight %}

E definimos a rota correspondente do formulário, no caso ajax `ckeditor_generic.routing.yml`:
{% highlight yml %}
ckeditor_generic.dialog:
  path: '/ckeditor_generic/dialog'
  defaults:
    _form: '\Drupal\ckeditor_generic\Form\CkeditorGenericDialog'
    _title: 'ckeditor_generic'
  options:
    _theme: ajax_base_page
  requirements:
    _permission: 'access in-place editing'
{% endhighlight %}

Vamos injetar código css/js tanto no modal quanto dentro do conteúdo
inserido no ckeditor, assim implementemos `ckeditor_generic.libraries.yml`:
{% highlight yml %}
ckeditor_generic:
  version: VERSION
  css:
    theme:
      css/ckeditor_generic.css: {}

ckeditor_generic.dialog:
  version: VERSION
  css:
    theme:
      css/dialog.css: {}
{% endhighlight %}

Em css/dialog.css eu injetei esse css:
{% highlight css %}
#editor-ckeditor-generic-dialog-form .form-item-attributes-body {
  clear: both;
  background-color: yellow;
}
{% endhighlight %}

E em ckeditor_generic.css:
{% highlight css %}
.ckeditor-generic{
    background-color: red;
    color: blue;
}

h1.ckeditor-generic-header {
    color: green;
}
{% endhighlight %}
Claro, essas cores foram usada só para verificar se o código está chegando onde
deveria estar chegando.

Por fim o `plugin.js` que trata da ação do botão em si:
{% highlight javascript %}

/**
 * @file
 * ckeditor_generic plugin.
 *
 * @ignore
 */

(function ($, Drupal, drupalSettings, CKEDITOR) {

    'use strict';
  
    CKEDITOR.plugins.add('ckeditor_generic', {
      init: function (editor) {
        editor.addCommand('ckeditor_generic', {
          modes: {wysiwyg: 1},
          canUndo: true,
          exec: function (editor) {

            // Prepare a save callback to be used upon saving the dialog.
            var saveCallback = function (returnValues) {
              editor.fire('saveSnapshot');
  
              if (returnValues.attributes.body) {
                var selection = editor.getSelection();
                var range = selection.getRanges(1)[0];
  
                if (range.collapsed) {
                  var values = returnValues.attributes;

                  var container = editor.document.createElement('div');
                  container.setAttribute('class', 'ckeditor-generic');
  
                  var header = editor.document.createElement('h1');
                  header.setAttribute('class', 'ckeditor-generic-header');

                  header.setHtml('parte de cima');
  
                  var body = editor.document.createElement('p');
                  body.setHtml(values.body);
  
                  container.append(header);
                  container.append(body);
  
                  editor.insertElement(container);

                }
                
              }
  
              // Save snapshot for undo support.
              editor.fire('saveSnapshot');
            };
            // Drupal.t() will not work inside CKEditor plugins because CKEditor
            // loads the JavaScript file instead of Drupal. Pull translated
            // strings from the plugin settings that are translated server-side.
            var dialogSettings = {
              title: editor.config.dialog_title_insert,
              dialogClass: 'ckeditor_generic-dialog'
            };
  
            // Open the dialog for the edit form.
            var existingValues = {};
            Drupal.ckeditor.openDialog(editor, Drupal.url('ckeditor_generic/dialog'), existingValues, saveCallback, dialogSettings);
          }
        });

        // Add button
        if (editor.ui.addButton) {
          editor.ui.addButton('ckeditor_generic_button', {
            label: Drupal.t('Insert ckeditor_generic'),
            command: 'ckeditor_generic',
            icon: this.path +  '../images/icone.png'
          });
        }
  
        // If the "menu" plugin is loaded, register the menu items.
        if (editor.addMenuItems) {
          editor.addMenuItems({
            ckeditor_generic: {
              label: Drupal.t('ckeditor_generic'),
              command: 'ckeditor_generic',
              group: 'tools',
              order: 1
            }
          });
        }
      }
    });
  
  })(jQuery, Drupal, drupalSettings, CKEDITOR);
{% endhighlight %}

