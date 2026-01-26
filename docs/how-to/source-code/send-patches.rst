.. meta::
   :description: Submit kernel patches to the Ubuntu kernel team mailing list. Learn formatting requirements, review process, and best practices for patches.

.. _how-to-send-patches:

How to send patches to the mailing-list
#######################################

To send kernel patches to the mailing-list, you should use the ``git
send-email`` command.

.. note::

    Most of the options explained here do not appear in the man page of
    ``git-send-email`` but ``git-format-patch`` instead. They however work the
    same.

You may want to create a specific identity for keeping common settings when
sending kernel patches. The commonly used settings are:

.. code-block:: shell

    git config set sendemail.ubuntu-kernel.chainReplyTo false
    git config set sendemail.ubuntu-kernel.suppresscc true
    git config set sendemail.ubuntu-kernel.thread true

    # And then include these settings with `--identity=ubuntu-kernel`
    git send-email --identity=ubuntu-kernel ...

Specify series
==============

All patches must be targeted at some series (unstable, noble, ...).
Specify the targeted series with the ``--subject-prefix`` option:

.. code-block:: shell

    git send-email --subject-prefix="SRU][O/N/J:linux-azure][PATCH" ...

The tags used in this example show that this patchset is targeting the
following kernels for an SRU update: *oracular*, *noble*, and
*jammy:linux-azure*.

Send a new version of a patchset
================================

Mistakes happen; we are all human. If you want to send a new version of your
patchset that fixes some issues, you can use the ``-v, --reroll-count`` option:

.. code-block:: shell

    git send-email --subject-prefix=... -v 2

This will generate ``[PATCH v2]`` instead of just ``[PATCH]`` to indicate that
this is a new revision of a patchset.

You should first make sure that your original patchset was rejected by having a
NAK/NACK in its thread. You can reply to the email saying that you will send a
new version of the patchset.

If you found a mistake you made, you can NAK and say that you will send a new
version in the same email.

In the cover letter of the new patchset, describe what was changed compared
to the previous submitted version.

.. seealso::

   - (Reference) :ref:`ubuntu-patches-acceptance-criteria`
