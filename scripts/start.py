import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

# Создаем модель нейросети
model = Sequential()
model.add(LSTM(128, input_shape=(max_len, len(chars))))
model.add(Dropout(0.5))
model.add(Dense(len(chars), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Обучаем нейросеть на обучающей выборке
model.fit(X_train, y_train, batch_size=128, epochs=100)

# Генерируем ответы на вопросы
def generate_answer(question):
    question = preprocess_question(question)
    X = prepare_input(question, maxlen, chars_indices)
    prediction = model.predict(X, verbose=0)[0]
    index = np.argmax(prediction)
    return indices_chars[index]
print(generate_answer("Hello"))