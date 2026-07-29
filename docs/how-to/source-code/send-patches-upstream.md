# How to send patches to the Linux kernel mailing-list

This guide shows you how to submit a change to the upstream Linux kernel. It assumes you have already made a code change, in a separate branch, that would benefit the wider kernel community.

```{note}
Ubuntu kernel maintainers prefer to apply changes to the Ubuntu kernel by cherry picking an upstream patch, which is why upstreaming matters. Ubuntu-specific changes (for example, Ubuntu kernel config changes) do not need to be submitted upstream.
```

1. **Read the submission process.** Read the [upstream patch submission documentation](https://docs.kernel.org/process/submitting-patches.html) and follow it accurately. If you need help, try asking other developers in the [Ubuntu Kernel room](https://matrix.to/#/#kernel:ubuntu.com) on the Ubuntu Matrix server.

2. **Match the coding style.** Make sure the change follows the upstream [kernel coding style](https://docs.kernel.org/process/coding-style.html).

3. **Test your kernel.** If you have a test kernel for an Ubuntu release, post a link to it on the relevant Launchpad bug and get it tested by the community.

4. **Choose the correct git tree.** If your change is in a subsystem, target that subsystem maintainer's tree (these are later merged into Linus's tree). Otherwise, clone Linus's tree:

   ```
   git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
   ```

5. **Commit and sign off.** Commit each logical change with a sign-off using `git commit -s`. Signing off adds a tag to the bottom of the commit message that marks you as being responsible for the code. 

   If a patch fixes a bug in a released kernel and should be backported, add a `Cc: stable@vger.kernel.org` line to the sign-off area of its commit message (NOT as an email recipient). Pair it with a `Fixes:` tag identifying the commit that introduced the bug where possible.
   ```{note}
   The upstream patch submission documentation describes other tags as well, such as `Closes:`, `Reported-by:`, `Suggested-by:`, `Tested-by:`, `Link:`, etc.. Add them as applicable.
   ```

6. **Generate patches.** To generate patches from the commits, run:
   ```
   git format-patch --base=<base> -o outgoing/ <base>..
   ```
   Replace `<base>` with the branch or tag you based your work on top of (for example `master`). `--base=<base>` records the base commit the patches are built on top of. `<base>..` generates one patch per commit on top of `<base>` (e.g. all commits in your branch).

   If you are sending more than one patch, add `--cover-letter` to also generate `outgoing/0000-cover-letter.patch`, which is used to describe the patchset overall. A single patch does not need a cover letter.

   ```{note}
    Both the cover letter and commit messages can be used to leave comments, so keep them distinct: 

    - **The commit messages** explain *this specific change*: the problem it solves, why it is needed, and any implementation details a reader needs to understand. Make it self-contained — do not rely on external links or earlier patch versions. It is copied verbatim into the permanent git changelog, so write it for someone reading `git log` years later.
    - **The cover letter** describes *the series as a whole*: The overall goal, how the patches fit together, and the testing performed. It is not recorded in git history — it exists only to give reviewers context on the mailing list.
    ```

7. **Find the recipients.** Run `get_maintainer.pl` against your patch to list the maintainers and developers to mail it to:

   ```
   ./scripts/get_maintainer.pl ./0001-your-patch.patch
   ```

   For example, a wireless driver patch produces a list such as:

   ```
   Ivo van Doorn <IvDoorn@gmail.com>
   Gertjan van Wingerde <gwingerde@gmail.com>
   "John W. Linville" <linville@tuxdriver.com>
   linux-wireless@vger.kernel.org
   users@rt2x00.serialmonkey.com
   netdev@vger.kernel.org
   linux-kernel@vger.kernel.org
   ```

8. **Send the patch.** Submit the patch as inline text in a plain text email with no attachments or hyperlinks. Many email applications do not send plain text by default, so the simplest way is to use `git send-email`, which formats each patch correctly and lets you derive the recipient list from `get_maintainer.pl`. An example command may look like:

   ```
   git send-email \
   --to linux-kselftest@vger.kernel.org \
   --to netdev@vger.kernel.org \
   --cc-cmd='./scripts/get_maintainer.pl --norolestats outgoing/0001-selftests-net-fix-test_1.patch' \
   --cc kernel.engineer@canonical.com \
   --no-chain-reply \
   outgoing/0000-cover-letter.patch \
   outgoing/0001-selftests-net-fix-test_1.patch \
   outgoing/0002-selftests-net-fix-test_2.patch
   ```

   In this example, `--cc-cmd` runs `get_maintainer.pl` to add the subsystem maintainers automatically, `--cc` adds your own address, and `--no-chain-reply` keeps every patch threaded as a reply to the cover letter rather than to the previous patch.

9. **Respond to feedback.** It's not uncommon for patches to be revised before being accepted. Typically this involves discussing potential changes with maintainers, then resubmitting a revised patchset.

   When you send a new revision of a patchset make it clear this is a revised submission (e.g. add 'PATCH v2' in the cover letter subject), add a changelog of what changed between versions (for example `v2: fixed refcount edge case in patch 3`) and a link to the previous version(s) on the mailing list. Put these in the cover letter, or below the `---` separator line for a single patch submission. Content below `---` is stripped when the patch is applied, so it never reaches the permanent changelog.
