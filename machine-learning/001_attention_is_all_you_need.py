# %% [markdown]
# # Attention Is All You Need - Transformer Implementation
# 
# This notebook implements the Transformer architecture from the seminal paper
# "Attention Is All You Need" by Vaswani et al. (2017). The Transformer is based
# solely on attention mechanisms, dispensing with recurrence and convolutions entirely.

# %%
import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# %% [markdown]
# ## 1. Model Architecture Overview
# 
# The Transformer follows an encoder-decoder structure using stacked self-attention
# and point-wise, fully connected layers. The encoder maps an input sequence of
# symbol representations to a sequence of continuous representations, and the decoder
# generates an output sequence one element at a time in an auto-regressive manner.

# %% [markdown]
# ## 2. Scaled Dot-Product Attention
# 
# The attention function maps a query and a set of key-value pairs to an output.
# The output is computed as a weighted sum of the values, where the weight is
# computed by a compatibility function of the query with the corresponding key.
# 
# $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
# 
# We scale by $\sqrt{d_k}$ because for large values of $d_k$, the dot products
# grow large in magnitude, pushing the softmax into regions with extremely small gradients.

# %%
def softmax(x, axis=-1):
    """Compute softmax values for each set of scores in x."""
    # Subtract max for numerical stability
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / np.sum(e_x, axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Scaled Dot-Product Attention.
    
    Args:
        Q: Queries with shape (..., seq_len_q, d_k)
        K: Keys with shape (..., seq_len_k, d_k)
        V: Values with shape (..., seq_len_v, d_v) where seq_len_k == seq_len_v
        mask: Optional mask with shape broadcastable to (..., seq_len_q, seq_len_k)
    
    Returns:
        output: Attention output with shape (..., seq_len_q, d_v)
        attention_weights: Attention weights with shape (..., seq_len_q, seq_len_k)
    """
    d_k = Q.shape[-1]
    
    # Compute attention scores: QK^T / sqrt(d_k)
    scores = np.matmul(Q, K.swapaxes(-2, -1)) / np.sqrt(d_k)
    
    # Apply mask if provided (for decoder self-attention)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    
    # Apply softmax to get attention weights
    attention_weights = softmax(scores, axis=-1)
    
    # Compute weighted sum of values
    output = np.matmul(attention_weights, V)
    
    return output, attention_weights

# %% [markdown]
# ### Demonstrate Scaled Dot-Product Attention

# %%
# Create sample Q, K, V matrices
seq_len = 4
d_k = 8
d_v = 8

Q = np.random.randn(seq_len, d_k)
K = np.random.randn(seq_len, d_k)
V = np.random.randn(seq_len, d_v)

output, attention_weights = scaled_dot_product_attention(Q, K, V)

print("Query shape:", Q.shape)
print("Key shape:", K.shape)
print("Value shape:", V.shape)
print("Output shape:", output.shape)
print("Attention weights shape:", attention_weights.shape)

# Visualize attention weights
plt.figure(figsize=(6, 5))
plt.imshow(attention_weights, cmap='Blues', aspect='auto')
plt.colorbar(label='Attention Weight')
plt.xlabel('Key Position')
plt.ylabel('Query Position')
plt.title('Scaled Dot-Product Attention Weights')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Multi-Head Attention
# 
# Instead of performing a single attention function, we linearly project the queries,
# keys and values h times with different learned linear projections. On each of these
# projected versions we perform the attention function in parallel, yielding d_v-dimensional
# output values. These are concatenated and projected again.
# 
# $$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O$$
# $$\text{where head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$
# 
# The paper uses h=8 parallel attention heads with d_k = d_v = d_model/h = 64.

# %%
class MultiHeadAttention:
    """
    Multi-Head Attention mechanism.
    
    In this work we employ h = 8 parallel attention layers, or heads.
    For each of these we use d_k = d_v = d_model/h = 64.
    """
    
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.d_v = d_model // num_heads
        
        # Initialize projection matrices
        # W_Q, W_K, W_V for each head, and W_O for output
        self.W_Q = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.W_K = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.W_V = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
        self.W_O = np.random.randn(d_model, d_model) * np.sqrt(2.0 / d_model)
    
    def split_heads(self, x):
        """Split the last dimension into (num_heads, d_k)."""
        batch_size = x.shape[0]
        seq_len = x.shape[1]
        # Reshape to (batch_size, seq_len, num_heads, d_k)
        x = x.reshape(batch_size, seq_len, self.num_heads, self.d_k)
        # Transpose to (batch_size, num_heads, seq_len, d_k)
        return x.transpose(0, 2, 1, 3)
    
    def combine_heads(self, x):
        """Combine heads back to original shape."""
        batch_size = x.shape[0]
        seq_len = x.shape[2]
        # Transpose from (batch_size, num_heads, seq_len, d_k) to (batch_size, seq_len, num_heads, d_k)
        x = x.transpose(0, 2, 1, 3)
        # Reshape to (batch_size, seq_len, d_model)
        return x.reshape(batch_size, seq_len, self.d_model)
    
    def forward(self, Q, K, V, mask=None):
        """
        Forward pass of multi-head attention.
        
        Args:
            Q: Queries (batch_size, seq_len_q, d_model)
            K: Keys (batch_size, seq_len_k, d_model)
            V: Values (batch_size, seq_len_v, d_model)
            mask: Optional mask
        
        Returns:
            output: (batch_size, seq_len_q, d_model)
            attention_weights: (batch_size, num_heads, seq_len_q, seq_len_k)
        """
        batch_size = Q.shape[0]
        
        # Linear projections
        Q_proj = np.matmul(Q, self.W_Q)  # (batch_size, seq_len_q, d_model)
        K_proj = np.matmul(K, self.W_K)  # (batch_size, seq_len_k, d_model)
        V_proj = np.matmul(V, self.W_V)  # (batch_size, seq_len_v, d_model)
        
        # Split into multiple heads
        Q_split = self.split_heads(Q_proj)  # (batch_size, num_heads, seq_len_q, d_k)
        K_split = self.split_heads(K_proj)  # (batch_size, num_heads, seq_len_k, d_k)
        V_split = self.split_heads(V_proj)  # (batch_size, num_heads, seq_len_v, d_v)
        
        # Apply scaled dot-product attention
        attention_output, attention_weights = scaled_dot_product_attention(
            Q_split, K_split, V_split, mask
        )
        
        # Combine heads
        concat_attention = self.combine_heads(attention_output)  # (batch_size, seq_len_q, d_model)
        
        # Final linear projection
        output = np.matmul(concat_attention, self.W_O)  # (batch_size, seq_len_q, d_model)
        
        return output, attention_weights

# %% [markdown]
# ### Demonstrate Multi-Head Attention

# %%
# Parameters from the paper
d_model = 512
num_heads = 8
batch_size = 2
seq_len = 10

# Create sample input
x = np.random.randn(batch_size, seq_len, d_model)

# Create multi-head attention layer
mha = MultiHeadAttention(d_model, num_heads)

# Self-attention: Q, K, V all come from the same source
output, attention_weights = mha.forward(x, x, x)

print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"Attention weights shape: {attention_weights.shape}")
print(f"Number of heads: {num_heads}")
print(f"d_k = d_v = d_model/h = {d_model // num_heads}")

# %% [markdown]
# ## 4. Position-wise Feed-Forward Networks
# 
# Each layer in the encoder and decoder contains a fully connected feed-forward network,
# applied to each position separately and identically. This consists of two linear
# transformations with a ReLU activation in between:
# 
# $$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$
# 
# The dimensionality of input and output is d_model = 512, and the inner-layer
# has dimensionality d_ff = 2048.

# %%
class PositionwiseFeedForward:
    """
    Position-wise Feed-Forward Network.
    
    The dimensionality of input and output is d_model = 512,
    and the inner-layer has dimensionality d_ff = 2048.
    """
    
    def __init__(self, d_model, d_ff):
        self.d_model = d_model
        self.d_ff = d_ff
        
        # Initialize weights
        self.W1 = np.random.randn(d_model, d_ff) * np.sqrt(2.0 / d_model)
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * np.sqrt(2.0 / d_ff)
        self.b2 = np.zeros(d_model)
    
    def forward(self, x):
        """
        Forward pass.
        
        Args:
            x: Input tensor (batch_size, seq_len, d_model)
        
        Returns:
            output: (batch_size, seq_len, d_model)
        """
        # First linear transformation + ReLU
        hidden = np.maximum(0, np.matmul(x, self.W1) + self.b1)
        # Second linear transformation
        output = np.matmul(hidden, self.W2) + self.b2
        return output

# %%
# Demonstrate FFN
d_model = 512
d_ff = 2048

ffn = PositionwiseFeedForward(d_model, d_ff)
x = np.random.randn(batch_size, seq_len, d_model)
output = ffn.forward(x)

print(f"FFN Input shape: {x.shape}")
print(f"FFN Output shape: {output.shape}")
print(f"Inner layer dimensionality: {d_ff}")

# %% [markdown]
# ## 5. Positional Encoding
# 
# Since the model contains no recurrence and no convolution, we must inject some
# information about the relative or absolute position of the tokens in the sequence.
# We add "positional encodings" to the input embeddings at the bottoms of the
# encoder and decoder stacks.
# 
# The paper uses sine and cosine functions of different frequencies:
# 
# $$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{model}})$$
# $$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{model}})$$
# 
# This was chosen because it allows the model to easily learn to attend by relative
# positions, since for any fixed offset k, PE_{pos+k} can be represented as a linear
# function of PE_{pos}.

# %%
def get_positional_encoding(max_seq_len, d_model):
    """
    Generate positional encoding using sine and cosine functions.
    
    Args:
        max_seq_len: Maximum sequence length
        d_model: Model dimension
    
    Returns:
        Positional encoding matrix of shape (max_seq_len, d_model)
    """
    PE = np.zeros((max_seq_len, d_model))
    position = np.arange(max_seq_len)[:, np.newaxis]
    
    # Compute the div_term: 10000^(2i/d_model)
    div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
    
    # Apply sin to even indices and cos to odd indices
    PE[:, 0::2] = np.sin(position * div_term)
    PE[:, 1::2] = np.cos(position * div_term)
    
    return PE

# %% [markdown]
# ### Visualize Positional Encoding

# %%
max_seq_len = 100
d_model = 512

PE = get_positional_encoding(max_seq_len, d_model)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot the full positional encoding matrix
im = axes[0].imshow(PE, cmap='RdBu', aspect='auto')
axes[0].set_xlabel('Dimension')
axes[0].set_ylabel('Position')
axes[0].set_title('Positional Encoding Matrix')
plt.colorbar(im, ax=axes[0])

# Plot specific dimensions
positions = np.arange(max_seq_len)
for dim in [0, 1, 2, 3, 100, 101]:
    axes[1].plot(positions, PE[:, dim], label=f'dim {dim}')
axes[1].set_xlabel('Position')
axes[1].set_ylabel('Encoding Value')
axes[1].set_title('Positional Encoding for Different Dimensions')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### Demonstrate that PE_{pos+k} can be represented as a linear function of PE_{pos}

# %%
# Show that positional encodings allow learning relative positions
# For a fixed offset k, PE_{pos+k} = f(PE_{pos}) where f is linear

k = 5  # offset
pos = 20  # base position
d = 4  # dimension to examine

# The relationship: sin(pos+k) = sin(pos)cos(k) + cos(pos)sin(k)
# This is a linear combination of sin(pos) and cos(pos)

print("Demonstrating linear relationship for relative positions:")
print(f"Position {pos}, offset k={k}")
print(f"\nFor dimension pair (2i, 2i+1):")

for i in range(3):
    dim_sin = 2 * i
    dim_cos = 2 * i + 1
    
    # Direct computation
    direct = PE[pos + k, dim_sin]
    
    # Linear combination
    div_term = np.exp(dim_sin * -(np.log(10000.0) / d_model))
    linear = PE[pos, dim_sin] * np.cos(k * div_term) + PE[pos, dim_cos] * np.sin(k * div_term)
    
    print(f"  Dim {dim_sin}: Direct PE[{pos+k}] = {direct:.6f}, Linear combination = {linear:.6f}")

# %% [markdown]
# ## 6. Layer Normalization
# 
# We employ layer normalization around each of the sub-layers.
# The output of each sub-layer is LayerNorm(x + Sublayer(x)).

# %%
class LayerNorm:
    """Layer Normalization."""
    
    def __init__(self, d_model, eps=1e-6):
        self.d_model = d_model
        self.eps = eps
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)
    
    def forward(self, x):
        """
        Apply layer normalization.
        
        Args:
            x: Input tensor (..., d_model)
        
        Returns:
            Normalized tensor
        """
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return self.gamma * (x - mean) / (std + self.eps) + self.beta

# %% [markdown]
# ## 7. Encoder Layer
# 
# Each encoder layer has two sub-layers:
# 1. Multi-head self-attention mechanism
# 2. Position-wise fully connected feed-forward network
# 
# We employ a residual connection around each of the two sub-layers,
# followed by layer normalization.

# %%
class EncoderLayer:
    """
    Single Transformer Encoder Layer.
    
    Each layer has two sub-layers:
    1. Multi-head self-attention
    2. Position-wise feed-forward network
    
    With residual connections and layer normalization.
    """
    
    def __init__(self, d_model, num_heads, d_ff, dropout_rate=0.1):
        self.self_attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionwiseFeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.dropout_rate = dropout_rate
    
    def dropout(self, x, training=True):
        """Apply dropout during training."""
        if training and self.dropout_rate > 0:
            mask = np.random.binomial(1, 1 - self.dropout_rate, x.shape) / (1 - self.dropout_rate)
            return x * mask
        return x
    
    def forward(self, x, mask=None, training=True):
        """
        Forward pass.
        
        Args:
            x: Input tensor (batch_size, seq_len, d_model)
            mask: Optional attention mask
            training: Whether in training mode
        
        Returns:
            output: (batch_size, seq_len, d_model)
        """
        # Self-attention with residual connection and layer norm
        attn_output, _ = self.self_attention.forward(x, x, x, mask)
        attn_output = self.dropout(attn_output, training)
        x = self.norm1.forward(x + attn_output)
        
        # Feed-forward with residual connection and layer norm
        ff_output = self.feed_forward.forward(x)
        ff_output = self.dropout(ff_output, training)
        x = self.norm2.forward(x + ff_output)
        
        return x

# %% [markdown]
# ## 8. Decoder Layer
# 
# The decoder has three sub-layers:
# 1. Masked multi-head self-attention (prevents attending to subsequent positions)
# 2. Multi-head attention over encoder output (encoder-decoder attention)
# 3. Position-wise feed-forward network

# %%
def create_look_ahead_mask(size):
    """
    Create a look-ahead mask to prevent attending to future positions.
    
    This masking, combined with the fact that output embeddings are offset
    by one position, ensures that predictions for position i can depend
    only on the known outputs at positions less than i.
    """
    mask = np.triu(np.ones((size, size)), k=1)
    return mask == 0  # True where we can attend, False where we mask

class DecoderLayer:
    """
    Single Transformer Decoder Layer.
    
    Each layer has three sub-layers:
    1. Masked multi-head self-attention
    2. Multi-head attention over encoder output
    3. Position-wise feed-forward network
    """
    
    def __init__(self, d_model, num_heads, d_ff, dropout_rate=0.1):
        self.self_attention = MultiHeadAttention(d_model, num_heads)
        self.enc_dec_attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionwiseFeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.norm3 = LayerNorm(d_model)
        self.dropout_rate = dropout_rate
    
    def dropout(self, x, training=True):
        """Apply dropout during training."""
        if training and self.dropout_rate > 0:
            mask = np.random.binomial(1, 1 - self.dropout_rate, x.shape) / (1 - self.dropout_rate)
            return x * mask
        return x
    
    def forward(self, x, encoder_output, look_ahead_mask=None, padding_mask=None, training=True):
        """
        Forward pass.
        
        Args:
            x: Decoder input (batch_size, target_seq_len, d_model)
            encoder_output: Encoder output (batch_size, input_seq_len, d_model)
            look_ahead_mask: Mask for self-attention
            padding_mask: Mask for encoder-decoder attention
            training: Whether in training mode
        
        Returns:
            output: (batch_size, target_seq_len, d_model)
        """
        # Masked self-attention
        self_attn_output, _ = self.self_attention.forward(x, x, x, look_ahead_mask)
        self_attn_output = self.dropout(self_attn_output, training)
        x = self.norm1.forward(x + self_attn_output)
        
        # Encoder-decoder attention
        # Queries come from decoder, keys and values from encoder
        enc_dec_attn_output, _ = self.enc_dec_attention.forward(x, encoder_output, encoder_output, padding_mask)
        enc_dec_attn_output = self.dropout(enc_dec_attn_output, training)
        x = self.norm2.forward(x + enc_dec_attn_output)
        
        # Feed-forward
        ff_output = self.feed_forward.forward(x)
        ff_output = self.dropout(ff_output, training)
        x = self.norm3.forward(x + ff_output)
        
        return x

# %% [markdown]
# ### Visualize Look-Ahead Mask

# %%
seq_len = 8
mask = create_look_ahead_mask(seq_len)

plt.figure(figsize=(6, 5))
plt.imshow(mask, cmap='Blues', aspect='auto')
plt.colorbar(label='Can Attend (1=Yes, 0=No)')
plt.xlabel('Key Position')
plt.ylabel('Query Position')
plt.title('Look-Ahead Mask for Decoder Self-Attention')
plt.tight_layout()
plt.show()

print("Look-ahead mask ensures position i can only attend to positions <= i")

# %% [markdown]
# ## 9. Full Transformer Model
# 
# The encoder is composed of a stack of N = 6 identical layers.
# The decoder is also composed of a stack of N = 6 identical layers.

# %%
class Transformer:
    """
    Full Transformer Model.
    
    The encoder is composed of a stack of N = 6 identical layers.
    The decoder is also composed of a stack of N = 6 identical layers.
    
    Base model parameters:
    - N = 6 layers
    - d_model = 512
    - d_ff = 2048
    - h = 8 heads
    - d_k = d_v = 64
    - P_drop = 0.1
    """
    
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=512, num_layers=6,
                 num_heads=8, d_ff=2048, max_seq_len=5000, dropout_rate=0.1):
        self.d_model = d_model
        self.num_layers = num_layers
        
        # Embeddings (multiply by sqrt(d_model) as per paper)
        self.src_embedding = np.random.randn(src_vocab_size, d_model) * np.sqrt(2.0 / d_model)
        self.tgt_embedding = np.random.randn(tgt_vocab_size, d_model) * np.sqrt(2.0 / d_model)
        
        # Positional encoding
        self.positional_encoding = get_positional_encoding(max_seq_len, d_model)
        
        # Encoder layers
        self.encoder_layers = [
            EncoderLayer(d_model, num_heads, d_ff, dropout_rate)
            for _ in range(num_layers)
        ]
        
        # Decoder layers
        self.decoder_layers = [
            DecoderLayer(d_model, num_heads, d_ff, dropout_rate)
            for _ in range(num_layers)
        ]
        
        # Final linear layer (shared with embedding as per paper)
        self.final_linear = self.tgt_embedding.T  # Weight tying
        
        self.dropout_rate = dropout_rate
    
    def dropout(self, x, training=True):
        """Apply dropout during training."""
        if training and self.dropout_rate > 0:
            mask = np.random.binomial(1, 1 - self.dropout_rate, x.shape) / (1 - self.dropout_rate)
            return x * mask
        return x
    
    def encode(self, src, src_mask=None, training=True):
        """
        Encode the source sequence.
        
        Args:
            src: Source token indices (batch_size, src_seq_len)
            src_mask: Source padding mask
            training: Whether in training mode
        
        Returns:
            encoder_output: (batch_size, src_seq_len, d_model)
        """
        seq_len = src.shape[1]
        
        # Embedding + positional encoding
        # In the embedding layers, we multiply weights by sqrt(d_model)
        x = self.src_embedding[src] * np.sqrt(self.d_model)
        x = x + self.positional_encoding[:seq_len]
        x = self.dropout(x, training)
        
        # Pass through encoder layers
        for layer in self.encoder_layers:
            x = layer.forward(x, src_mask, training)
        
        return x
    
    def decode(self, tgt, encoder_output, look_ahead_mask=None, src_mask=None, training=True):
        """
        Decode the target sequence.
        
        Args:
            tgt: Target token indices (batch_size, tgt_seq_len)
            encoder_output: Encoder output (batch_size, src_seq_len, d_model)
            look_ahead_mask: Look-ahead mask for self-attention
            src_mask: Source padding mask for encoder-decoder attention
            training: Whether in training mode
        
        Returns:
            decoder_output: (batch_size, tgt_seq_len, d_model)
        """
        seq_len = tgt.shape[1]
        
        # Embedding + positional encoding
        x = self.tgt_embedding[tgt] * np.sqrt(self.d_model)
        x = x + self.positional_encoding[:seq_len]
        x = self.dropout(x, training)
        
        # Pass through decoder layers
        for layer in self.decoder_layers:
            x = layer.forward(x, encoder_output, look_ahead_mask, src_mask, training)
        
        return x
    
    def forward(self, src, tgt, src_mask=None, training=True):
        """
        Full forward pass.
        
        Args:
            src: Source token indices (batch_size, src_seq_len)
            tgt: Target token indices (batch_size, tgt_seq_len)
            src_mask: Source padding mask
            training: Whether in training mode
        
        Returns:
            logits: Output logits (batch_size, tgt_seq_len, tgt_vocab_size)
        """
        # Create look-ahead mask for decoder
        tgt_seq_len = tgt.shape[1]
        look_ahead_mask = create_look_ahead_mask(tgt_seq_len)
        
        # Encode
        encoder_output = self.encode(src, src_mask, training)
        
        # Decode
        decoder_output = self.decode(tgt, encoder_output, look_ahead_mask, src_mask, training)
        
        # Final linear projection to vocabulary
        logits = np.matmul(decoder_output, self.final_linear)
        
        return logits

# %% [markdown]
# ### Create and Test the Transformer

# %%
# Model parameters (base model from paper)
src_vocab_size = 1000
tgt_vocab_size = 1000
d_model = 512
num_layers = 6
num_heads = 8
d_ff = 2048

# Create model
transformer = Transformer(
    src_vocab_size=src_vocab_size,
    tgt_vocab_size=tgt_vocab_size,
    d_model=d_model,
    num_layers=num_layers,
    num_heads=num_heads,
    d_ff=d_ff
)

# Test with sample data
batch_size = 2
src_seq_len = 10
tgt_seq_len = 8

src = np.random.randint(0, src_vocab_size, (batch_size, src_seq_len))
tgt = np.random.randint(0, tgt_vocab_size, (batch_size, tgt_seq_len))

# Forward pass
logits = transformer.forward(src, tgt, training=False)

print("Transformer Base Model Configuration:")
print(f"  - Number of layers (N): {num_layers}")
print(f"  - Model dimension (d_model): {d_model}")
print(f"  - Feed-forward dimension (d_ff): {d_ff}")
print(f"  - Number of heads (h): {num_heads}")
print(f"  - d_k = d_v = d_model/h: {d_model // num_heads}")
print(f"\nInput shapes:")
print(f"  - Source: {src.shape}")
print(f"  - Target: {tgt.shape}")
print(f"\nOutput logits shape: {logits.shape}")

# %% [markdown]
# ## 10. Learning Rate Schedule
# 
# The paper uses a custom learning rate schedule:
# 
# $$lrate = d_{model}^{-0.5} \cdot \min(step\_num^{-0.5}, step\_num \cdot warmup\_steps^{-1.5})$$
# 
# This corresponds to increasing the learning rate linearly for the first warmup_steps
# training steps, and decreasing it thereafter proportionally to the inverse square root
# of the step number. The paper uses warmup_steps = 4000.

# %%
def get_learning_rate(step, d_model=512, warmup_steps=4000):
    """
    Compute learning rate according to the paper's schedule.
    
    lrate = d_model^(-0.5) * min(step^(-0.5), step * warmup_steps^(-1.5))
    """
    step = max(step, 1)  # Avoid division by zero
    arg1 = step ** (-0.5)
    arg2 = step * (warmup_steps ** (-1.5))
    return (d_model ** (-0.5)) * min(arg1, arg2)

# Visualize learning rate schedule
steps = np.arange(1, 100001)
lrs = [get_learning_rate(s) for s in steps]

plt.figure(figsize=(10, 5))
plt.plot(steps, lrs)
plt.axvline(x=4000, color='r', linestyle='--', label='warmup_steps=4000')
plt.xlabel('Training Step')
plt.ylabel('Learning Rate')
plt.title('Transformer Learning Rate Schedule')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Peak learning rate at step 4000: {get_learning_rate(4000):.6f}")

# %% [markdown]
# ## 11. Simple Training Example
# 
# Let's demonstrate training on a simple copy task where the model learns to copy
# the input sequence to the output.

# %%
def cross_entropy_loss(logits, targets):
    """Compute cross-entropy loss."""
    # Softmax
    probs = softmax(logits, axis=-1)
    
    # Gather probabilities for target tokens
    batch_size, seq_len, vocab_size = logits.shape
    
    # Create one-hot encoding
    one_hot = np.zeros_like(logits)
    for b in range(batch_size):
        for s in range(seq_len):
            one_hot[b, s, targets[b, s]] = 1
    
    # Cross-entropy
    loss = -np.sum(one_hot * np.log(probs + 1e-9)) / (batch_size * seq_len)
    return loss

def generate_copy_data(batch_size, seq_len, vocab_size, pad_token=0, sos_token=1):
    """Generate data for copy task."""
    # Generate random sequences (excluding special tokens)
    src = np.random.randint(2, vocab_size, (batch_size, seq_len))
    
    # Target is the same as source, shifted right with SOS token
    tgt_input = np.concatenate([
        np.full((batch_size, 1), sos_token),
        src[:, :-1]
    ], axis=1)
    tgt_output = src
    
    return src, tgt_input, tgt_output

# %% [markdown]
# ### Training Loop Demonstration

# %%
# Small model for demonstration
small_vocab_size = 50
small_d_model = 64
small_num_layers = 2
small_num_heads = 4
small_d_ff = 128
seq_len = 8

# Create small transformer
small_transformer = Transformer(
    src_vocab_size=small_vocab_size,
    tgt_vocab_size=small_vocab_size,
    d_model=small_d_model,
    num_layers=small_num_layers,
    num_heads=small_num_heads,
    d_ff=small_d_ff
)

# Training parameters
num_epochs = 50
batch_size = 32
losses = []

print("Training on copy task...")
print(f"Model: {small_num_layers} layers, d_model={small_d_model}, {small_num_heads} heads")
print()

for epoch in range(num_epochs):
    # Generate batch
    src, tgt_input, tgt_output = generate_copy_data(batch_size, seq_len, small_vocab_size)
    
    # Forward pass
    logits = small_transformer.forward(src, tgt_input, training=True)
    
    # Compute loss
    loss = cross_entropy_loss(logits, tgt_output)
    losses.append(loss)
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss:.4f}")

# Plot training loss
plt.figure(figsize=(10, 5))
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Cross-Entropy Loss')
plt.title('Training Loss on Copy Task')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 12. Attention Visualization
# 
# Let's visualize the attention patterns learned by the model.

# %%
def visualize_attention(transformer, src, tgt, layer_idx=0, head_idx=0):
    """Visualize attention weights for a specific layer and head."""
    # Get encoder output
    encoder_output = transformer.encode(src, training=False)
    
    # Get attention weights from decoder
    seq_len = tgt.shape[1]
    look_ahead_mask = create_look_ahead_mask(seq_len)
    
    # Get embeddings
    x = transformer.tgt_embedding[tgt] * np.sqrt(transformer.d_model)
    x = x + transformer.positional_encoding[:seq_len]
    
    # Pass through decoder layers and collect attention
    for i, layer in enumerate(transformer.decoder_layers):
        if i == layer_idx:
            # Get self-attention weights
            _, self_attn_weights = layer.self_attention.forward(x, x, x, look_ahead_mask)
            # Get encoder-decoder attention weights
            x_after_self_attn = layer.norm1.forward(x + layer.self_attention.forward(x, x, x, look_ahead_mask)[0])
            _, enc_dec_attn_weights = layer.enc_dec_attention.forward(x_after_self_attn, encoder_output, encoder_output)
            break
        x = layer.forward(x, encoder_output, look_ahead_mask, training=False)
    
    return self_attn_weights, enc_dec_attn_weights

# Generate sample data
src_sample, tgt_sample, _ = generate_copy_data(1, seq_len, small_vocab_size)

# Get attention weights
self_attn, enc_dec_attn = visualize_attention(small_transformer, src_sample, tgt_sample, layer_idx=0)

# Plot attention weights
fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for head in range(min(4, small_num_heads)):
    # Self-attention
    axes[0, head].imshow(self_attn[0, head], cmap='Blues', aspect='auto')
    axes[0, head].set_title(f'Self-Attn Head {head}')
    axes[0, head].set_xlabel('Key Position')
    axes[0, head].set_ylabel('Query Position')
    
    # Encoder-decoder attention
    axes[1, head].imshow(enc_dec_attn[0, head], cmap='Greens', aspect='auto')
    axes[1, head].set_title(f'Enc-Dec Attn Head {head}')
    axes[1, head].set_xlabel('Encoder Position')
    axes[1, head].set_ylabel('Decoder Position')

plt.suptitle('Attention Weights Visualization', fontsize=14)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 13. Complexity Comparison
# 
# The paper compares different layer types in terms of:
# - Complexity per layer
# - Sequential operations
# - Maximum path length
# 
# | Layer Type | Complexity per Layer | Sequential Ops | Max Path Length |
# |------------|---------------------|----------------|-----------------|
# | Self-Attention | O(n² · d) | O(1) | O(1) |
# | Recurrent | O(n · d²) | O(n) | O(n) |
# | Convolutional | O(k · n · d²) | O(1) | O(log_k(n)) |

# %%
def compute_complexity(n_values, d=512, k=3):
    """Compute complexity for different layer types."""
    complexities = {
        'Self-Attention': [],
        'Recurrent': [],
        'Convolutional': []
    }
    
    for n in n_values:
        complexities['Self-Attention'].append(n**2 * d)
        complexities['Recurrent'].append(n * d**2)
        complexities['Convolutional'].append(k * n * d**2)
    
    return complexities

# Sequence lengths to compare
n_values = np.arange(10, 1001, 10)
d = 512

complexities = compute_complexity(n_values, d)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for layer_type, comp in complexities.items():
    plt.plot(n_values, np.array(comp) / 1e9, label=layer_type)
plt.xlabel('Sequence Length (n)')
plt.ylabel('Complexity (×10⁹)')
plt.title('Computational Complexity per Layer')
plt.legend()
plt.grid(True, alpha=0.3)

# When is self-attention faster?
crossover = d  # n² * d = n * d² when n = d
plt.axvline(x=crossover, color='r', linestyle='--', alpha=0.5)
plt.annotate(f'n = d = {d}', xy=(crossover, plt.ylim()[1]*0.8), fontsize=10)

plt.subplot(1, 2, 2)
# Maximum path length
path_lengths = {
    'Self-Attention': np.ones_like(n_values),
    'Recurrent': n_values,
    'Convolutional': np.log(n_values) / np.log(3)  # log_k(n) with k=3
}

for layer_type, path in path_lengths.items():
    plt.plot(n_values, path, label=layer_type)
plt.xlabel('Sequence Length (n)')
plt.ylabel('Maximum Path Length')
plt.title('Maximum Path Length Between Positions')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Key insight: Self-attention has O(1) maximum path length,")
print("making it easier to learn long-range dependencies.")

# %% [markdown]
# ## 14. Model Size Comparison
# 
# The paper presents two model configurations:
# - Base model: 65M parameters
# - Big model: 213M parameters

# %%
def count_parameters(d_model, d_ff, num_layers, num_heads, vocab_size):
    """Estimate number of parameters in the Transformer."""
    # Embedding parameters (shared between encoder, decoder, and output)
    embedding_params = vocab_size * d_model
    
    # Per encoder layer
    # Multi-head attention: 4 * d_model * d_model (Q, K, V, O projections)
    # FFN: d_model * d_ff + d_ff * d_model
    # Layer norms: 2 * 2 * d_model
    encoder_layer_params = 4 * d_model * d_model + 2 * d_model * d_ff + 4 * d_model
    
    # Per decoder layer (same as encoder + one more attention)
    decoder_layer_params = encoder_layer_params + 4 * d_model * d_model + 2 * d_model
    
    total = embedding_params + num_layers * (encoder_layer_params + decoder_layer_params)
    return total

# Base model
base_params = count_parameters(
    d_model=512, d_ff=2048, num_layers=6, num_heads=8, vocab_size=37000
)

# Big model
big_params = count_parameters(
    d_model=1024, d_ff=4096, num_layers=6, num_heads=16, vocab_size=37000
)

print("Model Parameter Counts:")
print(f"  Base model: ~{base_params / 1e6:.1f}M parameters")
print(f"  Big model:  ~{big_params / 1e6:.1f}M parameters")
print()
print("Paper reported:")
print("  Base model: 65M parameters")
print("  Big model:  213M parameters")

# %% [markdown]
# ## 15. Summary
# 
# This notebook implemented the key components of the Transformer architecture:
# 
# 1. **Scaled Dot-Product Attention**: The core attention mechanism with scaling by √d_k
# 2. **Multi-Head Attention**: Parallel attention heads for attending to different representation subspaces
# 3. **Position-wise Feed-Forward Networks**: Two-layer FFN applied to each position
# 4. **Positional Encoding**: Sinusoidal encodings to inject position information
# 5. **Encoder and Decoder Stacks**: N=6 identical layers with residual connections and layer normalization
# 6. **Learning Rate Schedule**: Warmup followed by inverse square root decay
# 
# Key advantages of the Transformer:
# - **Parallelization**: Unlike RNNs, all positions can be computed in parallel
# - **Constant path length**: O(1) maximum path length for learning long-range dependencies
# - **Interpretability**: Attention weights can be visualized to understand model behavior

# %%
print("=" * 60)
print("Transformer Architecture Summary")
print("=" * 60)
print()
print("Base Model Configuration:")
print("  - N (layers): 6")
print("  - d_model: 512")
print("  - d_ff: 2048")
print("  - h (heads): 8")
print("  - d_k = d_v: 64")
print("  - P_drop: 0.1")
print("  - warmup_steps: 4000")
print()
print("Key Equations:")
print("  Attention(Q,K,V) = softmax(QK^T / √d_k) V")
print("  MultiHead = Concat(head_1,...,head_h) W^O")
print("  FFN(x) = max(0, xW_1 + b_1) W_2 + b_2")
print("  PE(pos,2i) = sin(pos / 10000^(2i/d_model))")
print("  PE(pos,2i+1) = cos(pos / 10000^(2i/d_model))")

