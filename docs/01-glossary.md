# The words, in plain English

Read this once, then come back whenever a term appears.

- **Weights.** A model is a few hundred million to billions of numbers. Training
  means nudging those numbers.
- **Parameters, 0.8B, 2B.** The count of those numbers. 0.8B is 800 million.
- **Pretraining.** Reading most of the internet to predict the next word. A cluster
  job that produces a base model. We never do this.
- **Base model versus instruct model.** A base model only predicts text. An instruct
  model has been further trained to follow instructions. We start from an instruct
  model.
- **Fine-tuning.** Continuing to train an existing model on your own examples so it
  behaves your way. Full fine-tuning nudges every number and needs far more memory
  than a laptop has.
- **LoRA, Low-Rank Adaptation.** Freeze the big model, attach small trainable
  "sticky notes" called adapters to each layer, and train only those. The adapters
  for a 0.8B model are about 14 MB against 570 MB of frozen weights. You can swap or
  stack them.
- **QLoRA.** Same idea, but the frozen base is squashed to 4-bit first. This is what
  makes 8 GB of memory enough.
- **4-bit, quantisation.** Storing each weight with fewer digits. Smaller and faster,
  slightly less precise.
- **SFT, supervised fine-tuning.** Your examples are input and desired output pairs.
  Our whole dataset is that shape, one case per line in a text file.
- **Train, validation and test split.** The model learns from the training set.
  Validation tells you whether it is generalising or just memorising. The test set is
  touched once, at the end, so the final number is honest.
- **Loss.** How wrong the model is on average. Lower is better, up to a point.
- **Overfitting.** Training loss keeps falling but validation loss rises. The model
  is memorising. A lower validation loss did not mean better real accuracy in the
  project we studied, so we always score the actual task.
- **Epoch and iteration.** One pass over the whole training set is an epoch. One
  batch of examples is an iteration. We count iterations.
- **Learning rate.** How big each nudge is. Too big and training thrashes, too small
  and it crawls.
- **Batch size.** How many examples are processed per nudge. Bigger needs more
  memory. On 8 GB we use small batches.
- **Gradient checkpointing.** A trick that spends more computation to use less
  memory.
- **Distillation and synthetic data.** A strong teacher model writes the examples, a
  human checks a sample, a judge pass filters the rest. Risk: the student inherits
  the teacher's blind spots, which is why the hand-checked gold set exists.
- **Gold set.** Examples a human has checked by hand. The ground truth everything
  else is measured against.
- **Retrieval, RAG.** Looking facts up at answer time instead of training them in.
  We use a deterministic lookup table for dates and duties, which is the simplest
  form of this.
- **Adapter fusing.** Merging the LoRA sticky notes back into the base model so you
  have one ordinary model file.
- **GGUF.** The single-file format Ollama and llama.cpp run.
- **Ollama.** A program that runs models on your laptop and serves them to other
  programs.
- **Baseline.** The untuned model given the same prompt. Fine-tuning only counts if
  it beats this.
