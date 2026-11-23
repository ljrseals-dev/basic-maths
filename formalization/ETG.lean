import Mathlib

/-!
Epistolary Transfer Graph: foundational Lean 4 model.

This file formalizes structural invariants only. It does not certify that
recorded evidence is authentic, that an attribution is true, or that an
analyst's interpretation is legally admissible.
-/

namespace ETG

abbrev VertexId := Nat
abbrev EdgeId := Nat

inductive VertexKind
  | document | claim | motif | dataPacket | agent | activity
  deriving DecidableEq, Repr

inductive TransferType
  | precedence | influence | embedding | citation | modulation
  deriving DecidableEq, Repr

/-- Epistemic status of a recorded assertion; not a truth value. -/
inductive AssertionStatus
  | observed | inferred | disputed | unverified | withdrawn
  deriving DecidableEq, Repr

/-- A source reference is an identifier, not proof that the source is genuine. -/
structure SourceRef where
  sourceId : String
  locator : String
  digest : Option String := none
  deriving Repr, DecidableEq

structure Vertex where
  id : VertexId
  kind : VertexKind
  label : String := ""
  deriving Repr, DecidableEq

/-- Weight is a non-negative integer score. It is deliberately not called
    probability, truth, or evidential confidence. -/
structure Edge where
  id : EdgeId
  source : VertexId
  target : VertexId
  relation : TransferType
  weight : Nat
  status : AssertionStatus
  sourceRef : Option SourceRef := none
  deriving Repr, DecidableEq

structure Graph where
  vertices : List Vertex
  edges : List Edge
  deriving Repr

def hasVertex (g : Graph) (v : VertexId) : Prop :=
  v ∈ g.vertices.map Vertex.id

def hasEdgeId (g : Graph) (e : EdgeId) : Prop :=
  e ∈ g.edges.map Edge.id

def EdgeWellFormed (g : Graph) (e : Edge) : Prop :=
  hasVertex g e.source ∧ hasVertex g e.target

def UniqueVertexIds (g : Graph) : Prop :=
  (g.vertices.map Vertex.id).Nodup

def UniqueEdgeIds (g : Graph) : Prop :=
  (g.edges.map Edge.id).Nodup

def WellFormed (g : Graph) : Prop :=
  UniqueVertexIds g ∧ UniqueEdgeIds g ∧
  ∀ e, e ∈ g.edges → EdgeWellFormed g e

/-- Parallel edges are allowed: distinct edge identifiers may share endpoints. -/
def ParallelDistinct (e₁ e₂ : Edge) : Prop :=
  e₁.source = e₂.source ∧ e₁.target = e₂.target ∧ e₁.id ≠ e₂.id

/-- A path retains the actual edge instances, not merely a vertex sequence. -/
inductive EdgeWalk : VertexId → VertexId → List Edge → Prop
  | nil (v : VertexId) : EdgeWalk v v []
  | cons {u v w : VertexId} {e : Edge} {es : List Edge}
      (hsrc : e.source = u)
      (tail : EdgeWalk e.target v es) :
      EdgeWalk u v (e :: es)

def pathLength (es : List Edge) : Nat := es.length

def pathWeight (es : List Edge) : Nat :=
  es.foldl (fun total e => total + e.weight) 0

def pathTypeCount (es : List Edge) : Nat :=
  (es.map Edge.relation).eraseDups.length

theorem pathLength_nonnegative (es : List Edge) :
    0 ≤ (pathLength es : Int) := by
  simp [pathLength]

theorem pathWeight_nonnegative (es : List Edge) :
    0 ≤ (pathWeight es : Int) := by
  simp [pathWeight]

theorem empty_path_has_zero_length :
    pathLength [] = 0 := by rfl

theorem empty_path_has_zero_weight :
    pathWeight [] = 0 := by rfl

/-- The same source/target pair may carry distinct typed edge assertions. -/
theorem parallel_edges_preserve_identity
    (e₁ e₂ : Edge) (h : ParallelDistinct e₁ e₂) :
    e₁.id ≠ e₂.id := h.2.2

/-- Rational saturating normalization used in the exploratory spectral map. -/
def sigma (x : ℚ) : ℚ := x / (1 + x)

theorem sigma_nonnegative {x : ℚ} (hx : 0 ≤ x) :
    0 ≤ sigma x := by
  unfold sigma
  have hden : 0 < 1 + x := by linarith
  positivity

theorem sigma_lt_one {x : ℚ} (hx : 0 ≤ x) :
    sigma x < 1 := by
  unfold sigma
  have hden : 0 < 1 + x := by linarith
  rw [div_lt_one hden]
  linarith

structure SpectralTriple where
  f1 : ℚ
  f2 : ℚ
  f3 : ℚ
  deriving Repr

/-- The formula is parameter-level; no psychoacoustic claim is encoded. -/
def spectralMap (lengthFeature weightFeature typeFeature : ℚ)
    (lMax wMax : ℚ) : SpectralTriple :=
  { f1 := 250 + 600 * sigma (lengthFeature / lMax)
    f2 := 600 + 1800 * sigma (weightFeature / wMax)
    f3 := 2400 + 800 * sigma (typeFeature / 5) }

theorem spectralMap_f1_bounds
    (l w t lMax wMax : ℚ)
    (hl : 0 ≤ l) (hlMax : 0 < lMax) :
    250 ≤ (spectralMap l w t lMax wMax).f1 ∧
    (spectralMap l w t lMax wMax).f1 < 850 := by
  constructor
  · simp [spectralMap]
    have h := sigma_nonnegative (div_nonneg hl (le_of_lt hlMax))
    nlinarith
  · simp [spectralMap]
    have h := sigma_lt_one (div_nonneg hl (le_of_lt hlMax))
    nlinarith

theorem spectralMap_f2_bounds
    (l w t lMax wMax : ℚ)
    (hw : 0 ≤ w) (hwMax : 0 < wMax) :
    600 ≤ (spectralMap l w t lMax wMax).f2 ∧
    (spectralMap l w t lMax wMax).f2 < 2400 := by
  constructor
  · simp [spectralMap]
    have h := sigma_nonnegative (div_nonneg hw (le_of_lt hwMax))
    nlinarith
  · simp [spectralMap]
    have h := sigma_lt_one (div_nonneg hw (le_of_lt hwMax))
    nlinarith

theorem spectralMap_f3_bounds
    (l w t lMax wMax : ℚ)
    (ht : 0 ≤ t) :
    2400 ≤ (spectralMap l w t lMax wMax).f3 ∧
    (spectralMap l w t lMax wMax).f3 < 3200 := by
  constructor
  · simp [spectralMap]
    have h := sigma_nonnegative (div_nonneg ht (by norm_num : (0:ℚ) ≤ 5))
    nlinarith
  · simp [spectralMap]
    have h := sigma_lt_one (div_nonneg ht (by norm_num : (0:ℚ) < 5))
    nlinarith

end ETG
