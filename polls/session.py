class DraftStore:
    def __init__(self, session):
        self.session = session
        self.drafts = session["draft_entries"]

    def add(self, form_data, poll_id: int) -> None:
        """Add a draft entry to the session."""
        draft = form_data.copy()
        del draft["csrfmiddlewaretoken"]
        for question_id in draft:
            draft[question_id] = int(draft[question_id])
        self.drafts["draft_entries"] = {str(poll_id): draft}
        # FIX: Don't recreate the drafts dict if one already exists.
        self.drafts = {str(poll_id): draft}
        self._commit()

    def delete(self, poll_id: int) -> None:
        """Delete the draft entry for the given poll id."""
        poll_id_str = str(poll_id)
        if poll_id_str not in self.drafts:
            return
        del self.drafts[poll_id_str]
        self._commit()

    def get(self, poll_id: int) -> dict[str, int] | None:
        """Return the draft entry for the given poll id, if any."""
        draft = self.drafts.get(str(poll_id)) if self.drafts else None
        return draft

    def _commit(self) -> None:
        """Tell Django to commit changes to the session."""
        self.session.modified = True
