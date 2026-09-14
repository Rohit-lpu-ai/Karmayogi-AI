"""Model registry: importing this module registers every table on ``Base.metadata``.

Alembic's env.py and the test suite import it so autogenerate sees all models.
Each module's ``models.py`` is added here when the module gains tables.
"""

from app.modules.competency import models as competency_models  # noqa: F401
from app.modules.content import models as content_models  # noqa: F401
from app.modules.governance import models as governance_models  # noqa: F401
from app.modules.identity import models as identity_models  # noqa: F401
from app.modules.organization import models as organization_models  # noqa: F401
from app.modules.platform import models as platform_models  # noqa: F401
from app.modules.recommendation import models as recommendation_models  # noqa: F401
from app.modules.assessment import models as assessment_models  # noqa: F401
